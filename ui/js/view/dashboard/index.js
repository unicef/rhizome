'use strict';

var _ = require('lodash');
var api = require('../../data/api.js');
var lineChart = require('../../component/line-chart');

module.exports = {
	template: require('./template.html'),
	data: function () {
		return {
			missed: [],
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

					series[ind.indicator].push([d.campaign, Number(ind.value)]);
				}
			}

			self.missed = _.values(series);
		});
	},
	components: {
		'vue-line-chart': lineChart
	}
};
