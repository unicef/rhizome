/* global window */
'use strict';

var _      = require('lodash');
var moment = require('moment');

var api             = require('data/api');
var format          = require('util/format');
var indexIndicators = require('data/transform/indexIndicators');
var variables       = require('data/transform/variables');
var util            = require('util/data');

function normalize(d) {
	var total = _(d.indicators).values().sum();

	if (total === 0) {
		return d;
	}

	_.each(d.indicators, function (v, k) {
		d.indicators[k] /= total;
	});

	return d;
}

module.exports = {
	template : require('./district.html'),

	data : function () {
		return {
			campaign : null,
			columns  : [],
			region   : null,
			series   : []
		};
	},

	methods : {
		error : function () {
			window.alert('Dammit!');
		},

		load : function () {
			this.loading = true;

			if (!(this.campaign && this.region)) {
				return;
			}

			var indicators = [
				431,432,433,  // Immunity gap
				475,166,164,167,165, // Missed Children
				222, // Microplans
				187,189, // Conversions
				// FIXME: Transit points in place and with SM
				178,228,179,184,180,185,230,226,239, // Capacity to Perform
				194,219,173,172, // Supply
				245,236,192,193,191, // Polio+
				169,233, // Resources
				174, // Access plan
				442,443,444,445,446,447,448,449,450 // Inaccessibility
			];

			var datapoints = api.datapoints({
				parent_region__in : this.region.id,
				level             : 'district',
				indicator__in     : indicators,
				campaign_start    : moment(this.campaign.start_date).format('YYYY-MM-DD'),
				campaign_end      : moment(this.campaign.end_date).format('YYYY-MM-DD')
			});

			var self = this;

			Promise.all([api.indicators({ id__in : indicators }), datapoints])
				.then(function (data) {
					var indicatorIdx = _.indexBy(data[0].objects, 'id');
					var columns = _.map(indicators, function (id) {
						return indicatorIdx[id].short_name;
					});

					var data = _.map(data[1].objects, function (d) {
						var dataIdx = _.indexBy(d.indicators, 'indicator');

						return {
							name : d.region,
							values : _.map(indicators, function (id) {
								var v = null;

								if (dataIdx[id]) {
									v = dataIdx[id].value
								}

								return v;
							})
						};
					});

					self.indicators = columns;
					self.series     = data;
				}, this.error);
		}
	},

	watch : {
		campaign : 'load',
		region   : 'load'
	}
};
