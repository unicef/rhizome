'use strict';

var _        = require('lodash');
var moment   = require('moment');

var api      = require('../../data/api');
var dateUtil = require('../../util/date');

function campaignComparator(a, b) {
	if (!b.campaign) {
		return a.campaign ? -1 : 0;
	}

	return (a.campaign.start_date < b.campaign.start_date) ? -1 :
		(a.campaign.start_date > b.campaign.start_date) ? 1 : 0;
}

function dataError(err) {
	console.log(err);

	this.loading = false;
	this.error   = true;
}

function parseData(data) {
	var loaded = _.omit(data, 'objects');

	// Convert the data from an array of unique (region, campaign) objects
	// with multiple indicators into an array of objects for each
	// (region, campaign, indicator) set. This is is identical to the form in
	// which the data is stored in the datapoint table on the server, and is
	// more flexible for plotting because it's easier to access values and
	// facet on properties like indicator for creating multiple series.
	loaded.objects = _(data.objects).map(function (o) {
		var datapoints = [];
		var indicators = o.indicators;
		var props      = _.omit(o, 'indicators');

		for (var i = indicators.length - 1; i >= 0; i--) {
			var datum = indicators[i];

			datapoints.push(_.assign({
				indicator: datum.indicator,
				value    : datum.value
			}, props));
		}

		return datapoints;
	})
		.flatten()
		.sortBy(campaignComparator)
		.value();

	this.datapoints = loaded.objects;
	this.loading    = false;
}

function _loadIndicator () {
	console.debug('with-indicator::loadIndicator', this.indicator);

	var self = this;

	if (!this.indicators) {
		return;
	}

	var indicators = this.indicators;

	if (_.isString(indicators)) {
		indicators = JSON.parse(indicators);
	}

	if (!_.isArray(indicators)) {
		indicators = [indicators];
	}

	indicators = indicators.filter(function (d) {
		return _.isNumber(d) || _.isString(d);
	});

	if (indicators.length < 1) {
		// All indicators have been loaded. Begin loading the datapoints.
		this._loadDatapoints();
		return;
	}

	this.loading = true;

	api.indicators({ id__in: indicators })
		.then(function (data) {
			self.indicators = data.objects;
		}, dataError.bind(this));

	console.debug('with-indicator::loadIndicator', 'exit');
}

function _loadDatapoints () {
	console.info('with-indicator::loadDatapoints', 'enter');

	if (!this.indicators || !this.campaign || !this.region) {
		console.info('with-indicator::loadDatapoints', 'exit', 'missing parameters');
		return;
	}

	var q = {
		indicator__in: _.pluck(this.indicators, 'id'),
		campaign_end : this.campaign.end,
		region__in   : [this.region]
	};

	var start = this.campaign_start;
	if (start) {
		q.campaign_start = start;
	}

	console.debug('with-indicator::data-load', 'q', q);

	api.datapoints(q).then(parseData.bind(this), dataError.bind(this));
	console.info('with-indicator::loadDatapoints', 'exit');
}

module.exports = {

	paramAttributes: [
		'data-indicators',
		'data-period'
	],

	data: function () {
		return {
			campaign  : null,
			datapoints: [],
			error     : false,
			indicators: null,
			loading   : true,
			region    : null,
			period    :null
		};
	},

	created: function () {
		// Initialize private methods
		this._loadIndicator  = _loadIndicator.bind(this);
		this._loadDatapoints = _loadDatapoints.bind(this);

		this.$watch('campaign', this._loadDatapoints);
		this.$watch('region', this._loadDatapoints);

		this.$watch('indicators', this._loadIndicator);
		this._loadIndicator();
	},

	computed: {

		campaign_start: function () {
			if (!this.period) {
				return null;
			}

			var start = moment(this.campaign.date, 'YYYYMMDD');

			return start.subtract.apply(
					start,
					dateUtil.parseDuration(this.period)
				).format('YYYY-MM-DD');
		},

		length: function () {
			var datapoints = this.datapoints;

			return (datapoints && datapoints.length) || 0;
		},

		empty: function () {
			return this.length < 1;
		}

	}

};
