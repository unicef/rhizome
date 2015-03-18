/* global window */
'use strict';

var _    = require('lodash');
var path = require('vue/src/parsers/path');

var api  = require('data/api');
var util = require('util/data');

function onError(err) {
	window.alert('We\'re sorry, we failed to load some of the data for the dashboard.');
	console.error(err.msg);
	console.error(err.stack);
}

function getIndicator(d) {
	return d.indicator.short_name;
}

function getRegion(d) {
	return d.region;
}

function mapProperties(mapping) {
	return function (d) {
		var datum = _.clone(d);

		_.forEach(mapping, function (to, from) {
			path.set(datum, to, path.get(datum, from));
		});

		return datum;
	}
}

function makeSeries(getSeries) {
	return function (data) {
		return _(data)
			.groupBy(getSeries)
			.map(function (v, k) {
				return {
					name   : k,
					values : v
				};
			})
			.value();
		}
}

function formatData(datapoints, indicators, properties, series) {
	return _(datapoints)
		.pick(indicators)
		.values()
		.flatten()
		.map(mapProperties(properties))
		.thru(makeSeries(series))
		.value();
}

module.exports = {
	template: require('./nco.html'),

	data: function () {
		return {
			region        : null,
			campaign      : null,

			overview      : {
				missed : {
					inside  : [],
					outside : []
				},
				awareness       : [],
				influencer      : {
					domain : [0, 1],
					series : []
				},
				source          : {
					domain : [0, 1],
					series : []
				},
				reasonForMissed : {
					domain : [0, 1],
					series : []
				},
				absence         : {
					domain : [0, 1],
					series : []
				},
				noncompliance   : {
					domain : [0, 1],
					series : []
				},
				resolutions     : {
					domain : [0, 1],
					series : []
				}
			},
			missed : {
				reasons    : [],
				monitoring : [],
			},
			absences      : [],
			noncompliance : [],
			resolutions   : [],
			influencers   : [],
			sources       : []
		};
	},

	created: function () {
		this.fetch();
	},

	methods: {
		fetch: function () {
			if (!(this.campaign && this.region)) {
				return;
			}

			var indicators = [252,253,254,255,256,257,258,259,260,261,262,263,272,274,
				276,287,288,289,290,291,292,293,294,307,308,309,310,311,312,313,314,315,
				316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,
				334,345,346,347,348];

			var indicatorDefinitions = api.indicators({
				id__in : indicators
			});

			var overview = {
				region__in     : [this.region],
				indicator__in  : indicators,
				campaign_start : this.campaign.end,
				campaign_end   : this.campaign.end
			};

			var provinces = {
				parent_region__in : [this.region],
				indicator__in     : indicators,
				campaign_start    : this.campaign.end,
				campaign_end      : this.campaign.end,
				level             : 'province'
			};

			var overviewData = api.datapoints(overview);

			var self = this;

			Promise.all([indicatorDefinitions, overviewData])
				.then(function (data) {
					var indicators = _.indexBy(data[0].objects, 'id');
					var datapoints = _(data[1])
						.thru(util.unpivot)
						.forEach(function (d) {
							d.indicator = indicators[d.indicator];
						})
						.groupBy(function (d) {
							return d.indicator.id;
						});

					var barChartMapping = {
						'value'                : 'x',
						'indicator.short_name' : 'y'
					};

					self.overview.influencer.series = formatData(
						datapoints,
						[287,288,289,290,291,292,293,294],
						barChartMapping,
						getRegion);

					self.overview.source.series = formatData(
						datapoints,
						[307,308,309,310,311,312,313,314,315,316,317],
						barChartMapping,
						getRegion);

					self.overview.reasonForMissed.series = formatData(
						datapoints,
						[318,319,320,321,322],
						barChartMapping,
						getRegion);

					self.overview.absence.series = formatData(
						datapoints,
						[323,324,325,326,327],
						barChartMapping,
						getRegion);

					self.overview.noncompliance.series = formatData(
						datapoints,
						[328,329,330,331,332,333,334],
						barChartMapping,
						getRegion);

					self.overview.resolutions.series = formatData(
						datapoints,
						[345,346,347,348],
						barChartMapping,
						getRegion);
				}, onError);

			var provinceData = api.datapoints(provinces);

			Promise.all([indicatorDefinitions, provinceData])
				.then(function (data) {
					var indicators = _.indexBy(data[0], 'id');
					var datapoints = util.unpivot(data[1]);
				}, onError);
		}
	},

	watch: {
		'campaign' : 'fetch',
		'region'   : 'fetch'
	}
};
