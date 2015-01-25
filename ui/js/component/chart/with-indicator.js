'use strict';

var _        = require('lodash');
var moment   = require('moment');

var api      = require('../../data/api');
var dateUtil = require('../../util/date');

function campaignComparator(a, b, arr) {
	if (arr.length < 2) {
		return -1;
	}

	return (a.campaign.start_date < b.campaign.start_date) ? -1 :
		(a.campaign.start_date > b.campaign.start_date) ? 1 : 0;
}

function dataError(err) {
	console.log(err);
	this.$emit('data-load-error', err);
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
				value: datum.value
			}, props));
		}

		return datapoints;
	})
		.flatten()
		.sortBy(campaignComparator)
		.value();

	this.$emit('data-loaded', loaded);
}

module.exports = {
	created: function () {
		console.debug('with-indicator::created', 'enter');
	},

	events: {
		'data-indicator-load': function () {
			console.debug('with-indicator::loadIndicator', this.indicator);

			var self = this;

			if (!this.indicator) {
				return;
			}

			api.indicators({ id: this.indicator })
				.then(function (data) {
					self.indicator = data.objects[0];
				}, dataError.bind(this));
		},

		'data-load': function () {
			console.info('with-indicator::data-load', 'enter');
			var q = {
				indicator__in: [this.indicator.id],
				campaign_end : this.campaign.end,
				region__in   : [this.region]
			};

			if (this.period) {
				var start = moment(this.campaign.date, 'YYYYMMDD');

				q.campaign_start = start.subtract.apply(
						start,
						dateUtil.parseDuration(this.period)
					).format('YYYY-MM-DD');
			}

			console.debug('with-indicator::data-load', 'q', q);

			api.datapoints(q).then(parseData.bind(this), dataError.bind(this));
			console.info('with-indicator::data-load', 'exit');
		},
	}

};
