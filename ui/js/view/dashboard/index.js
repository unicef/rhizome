'use strict';

var _   = require('lodash');
var api = require('../../data/api.js');

module.exports = {
	template: require('./template.html'),
	replace: true,

	data: function () {
		return {
			missed     : [],
			immunityGap: [],
			microplans : {
				data    : [],
				socialData: 'NA',
				total     : 'NA'
			}
		};
	},

	created: function () {
		var self = this;

		// FIXME: This entire definition needs to be moved elsewhere and dynamically
		// generate regions and campaign information. The dashboard component should
		// load dashboard definitions to process and convert to UI, not fetch hard-
		// coded indicators and stuff them into hard-coded VM properties.

		// Fetch missed children for Borno.
		api.datapoints({
			limit        : 0,
			indicator__in: [21, 22, 25],
			region       : 13,
			uri_display  : 'id'
		}).done(function (data) {
			var series = {};

			for (var i = data.objects.length - 1; i >= 0; i--) {
				var d = data.objects[i];

				for (var j = d.indicators.length - 1; j >= 0; j--) {
					var ind = d.indicators[j];

					if (!series.hasOwnProperty(ind.indicator)) {
						series[ind.indicator] = [];
					}

					series[ind.indicator].push({
						x: d.campaign,
						y: Number(ind.value)
					});
				}
			}

			self.missed = _.values(_.pick(series, '21', '22'));
			self.immunityGap = [series[25]];
		});

		api.datapoints({
			limit        : 2,
			indicator__in: [27, 28],
			uri_display  : 'id'
		}).done(function (data) {
			var indicators = _.reduce(data.objects[0].indicators, function (r, v) {
				r[v.indicator] = Number(v.value);
				return r;
			}, {});

			self.microplans.data = [{
				value: indicators[28],
				color: '#5F6566',
			}, {
				value: indicators[27] - indicators[28],
				color: '#D5DFE2'
			}];

			self.microplans.socialData = indicators[28];
			self.microplans.total      = indicators[27];
		});
	},

	components: {
		'chart-base': require('../../component/chart'),
		'chart-line': require('../../component/chart/line'),
		'chart-pie' : require('../../component/chart/pie')
	}
};
