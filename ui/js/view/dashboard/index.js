'use strict';

var _ = require('lodash');
var api = require('../../data/api.js');

var chart = require('../../component/chart');

module.exports = {
	template: require('./template.html'),
	replace: true,

	data: function () {
		return {
			missed: [],
			immunityGap: []
		};
	},
	created: function () {
		var self = this;

		// Fetch missed children for Borno.
		api.datapoints({
			limit: 0,
			indicator__in: [21, 22, 25],
			region: 13,
			uri_display: 'id'
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
	},
	components: {
		'chart-base': chart,
		'chart-line': require('../../component/line-chart')
	}
};
