'use strict';

var _        = require('lodash');
var api      = require('../../data/api.js');

var coolgray = require('../../colors/coolgray');

module.exports = {
	template: require('./template.html'),
	replace: true,

	data: function () {
		return {
			polio      : [],
			missed     : [],
			immunityGap: [],
			microplans : {
				data      : [],
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

			self.polio = _.values(_.pick(series, '21', '22'));
			self.immunityGap = [series[25]];
		});

		// Just fetch a random pair of total microplans and microplans with social
		// data for demoing.
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
				// Indicator 27 is the total number of microplans. For the pie chart we
				// need the number of plans with data, and the number without, so we
				// subtract the total from those with.
				value: indicators[27] - indicators[28],
				color: '#D5DFE2'
			}];

			self.microplans.socialData = indicators[28];
			self.microplans.total      = indicators[27];
		});

		api.datapoints({
			limit        : 0,
			indicator__in: [22, 24, 26],
			region       : 13,
			uri_display  : 'id'
		}).done(function (data) {
			var layers = {};
			var color  = -1;

			// Transform the returned data for easy use with d3's stack layout. Each
			// indicator will correspond to one layer. Layers are represented by
			// objects with a name property and a values property, which is an array
			// of objects containing x and y properties. The campaign ID gets mapped
			// to the x property, and the indicator value goes into the y property.
			for (var i = data.objects.length - 1; i >= 0; i--) {
				var row = data.objects[i];

				for (var j = row.indicators.length - 1; j >= 0; j--) {
					var indicator = row.indicators[j].indicator;

					if (!layers.hasOwnProperty(indicator)) {
						layers[indicator] = {
							'name'  : indicator,
							'color' : coolgray[++color % coolgray.length],
							'values': []
						};
					}

					layers[indicator].values.push({
						x: row.campaign,
						y: Number(row.indicators[j].value)
					});
				}
			}

			self.missed = _.values(layers);
		});
	},

	components: {
		'chart-base'   : require('../../component/chart'),
		'chart-line'   : require('../../component/chart/line'),
		'chart-pie'    : require('../../component/chart/pie'),
		'chart-stacked': require('../../component/chart/stacked')
	}
};
