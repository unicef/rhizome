/* global window */
'use strict';

var _      = require('lodash');
var d3     = require('d3');
var React  = require('react');
var moment = require('moment');
var path   = require('vue/src/parsers/path');

var Chart                = require('component/Chart.jsx');
var ToggleableStackedBar = require('dashboard/ToggleableStackedBar.jsx');

var api    = require('data/api');
var util   = require('util/data');

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
	};
}

function filterMissing(data) {
	return _(data)
		.groupBy('y')
		.filter(function (v) {
			return _(v).pluck('x').some(_.partial(util.defined, _, _.identity));
		})
		.values()
		.flatten()
		.forEach(function (d) {
			if (!util.defined(d.x)) {
				d.x = 0;
			}
		})
		.value();
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
		};
}

function formatData(datapoints, indicators, properties, series) {
	return _(datapoints)
		.pick(indicators)
		.values()
		.flatten()
		.map(mapProperties(properties))
		.thru(filterMissing)
		.thru(makeSeries(series))
		.value();
}

function value(datapoint) {
	if (datapoint && datapoint.hasOwnProperty('value')) {
		return datapoint.value;
	}

	return null;
}

function barChart (el, title, datapoints, indicators, properties, series) {
	var data = formatData(datapoints, indicators, properties, series);

	var props = {
		data  : data,
		title : title
	};

	var chart = React.createElement(ToggleableStackedBar, props);

	React.render(chart, el);
}

module.exports = {
	template: require('./nco.html'),

	data: function () {
		return {
			region        : null,
			campaign      : null,

			overview      : {
				loading : true,
				missed  : {
					inside       : [],
					outside      : [],
					insideLabel  : '',
					outsideLabel : ''
				},
				inside         : [],
				outside        : [],
				awareness      : [],
				awarenessLabel : '',
				missedVsAwareness : {
					inside  : [],
					outside : [],
					range   : [0, 1]
				},
				influencer : {
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
				barHeight  : 6,
				offset     : 'zero'
			},
			absences      : {
				reasons : [],
				offset  : 'zero'
			},
			noncompliance : {
				reasons : [],
				offset  : 'zero',
			},
			resolutions   : {
				by     : [],
				offset : 'zero',
			},
			influencers   : {
				by     : [],
				offset : 'zero',
			},
			sources       : {
				series : [],
				offset : 'zero'
			}
		};
	},

	created: function () {
		this._regionIndex = api.regions().then(function (data) {
			return _.indexBy(data.objects, 'id');
		}, onError);

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
				334,345,346,347,348,267,268,251,264,266,265,273,295,299,303,296,300,304,
				297,301,305,298,302,278,279,280,281,282,283,284,285,340,341,342,343,252,
				255,258,261,253,256,259,254,257,260,263,262,246,247,248,249,250];

			var indicatorDefinitions = api.indicators({
				id__in : indicators
			});

			var overview = {
				region__in     : [this.region.id],
				indicator__in  : indicators,
				campaign_start : moment(this.campaign.start_date).format('YYYY-MM-DD'),
				campaign_end   : moment(this.campaign.end_date).format('YYYY-MM-DD')
			};

			var provinces = {
				parent_region__in : [this.region.id],
				indicator__in     : indicators,
				campaign_start    : moment(this.campaign.start_date).format('YYYY-MM-DD'),
				campaign_end      : moment(this.campaign.end_date).format('YYYY-MM-DD'),
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

					self.overview.loading       = false;
					self.overview.missed.inside = datapoints
						.pick(272)
						.values()
						.flatten()
						.value();

					var fmt = function (d) {
						if (d < 0.01 && d > 0) {
							return '< 1%';
						}

						return d3.format('%')(d);
					};

					self.overview.missed.insideLabel = fmt(value(self.overview.missed.inside[0]));

					self.overview.missed.outside = datapoints
						.pick(274)
						.values()
						.flatten()
						.value();

					self.overview.missed.outsideLabel = fmt(value(self.overview.missed.outside[0]));

					self.overview.awareness = datapoints
						.pick(276)
						.values()
						.flatten()
						.value();

					self.overview.awarenessLabel = fmt(value(self.overview.awareness[0]));

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


			var provinceData  = api.datapoints(provinces);
			var regionMapping = {
				'value'       : 'x',
				'region.name' : 'y'
			};

			Promise.all([indicatorDefinitions, provinceData, this._regionIndex])
				.then(function (data) {
					var indicators = _.indexBy(data[0].objects, 'id');
					var regions    = data[2];
					var datapoints = _(data[1])
						.thru(util.unpivot)
						.forEach(function (d) {
							d.indicator = indicators[d.indicator];
							d.region    = regions[d.region];
						})
						.groupBy(function (d) {
							return d.indicator.id;
						});

					// Set the same range for both scatter plots
					var domain = d3.extent(_(data[1].objects)
						.pluck('indicators')
						.flatten()
						.filter(function (d) { return d.indicator == 276; })
						.pluck('value')
						.value()
					);

					var range = d3.extent(_(data[1].objects)
						.pluck('indicators')
						.flatten()
						.filter(function (d) { return d.indicator == 272 || d.indicator == 274; })
						.pluck('value')
						.value()
					);

					// Inside x = 276, y = 272
					var inside = _(data[1].objects)
						.map(function (d) {
							var index = _.indexBy(d.indicators, 'indicator');

							return {
								id   : d.region,
								name : regions[d.region].name,
								x    : value(index[276]),
								y    : value(index[272])
							};
						})
						.filter(function (d) {
							return _.isFinite(d.x) && _.isFinite(d.y);
						})
						.value();

					var showTooltip = function (d, i, el) {
						var evt = d3.event;

						self.$dispatch('tooltip-show', {
							el       : el,
							position : {
								x : evt.pageX,
								y : evt.pageY
							},
							data : {
								// Have to make sure we use the default tooltip, otherwise if a
								// different template was used, this shows the old template
								template : 'tooltip-default',
								text     : d.name,
								delay    : 0
							}
						});
					};

					var hideTooltip = function (d, i, el) {
						self.$dispatch('tooltip-hide', { el : el });
					};

					var options = {
						aspect      : 1.7,
						domain      : _.constant(domain),
						onMouseOut  : hideTooltip,
						onMouseOver : showTooltip,
						range       : _.constant(range),
						xFormat     : d3.format('%'),
						xLabel      : 'Caregiver Awareness',
						yFormat     : d3.format('%'),
						yLabel      : 'Missed Children'
					};

					React.render(
						React.createElement(Chart, {
							type    : 'ScatterChart',
							data    : inside,
							options : options
						}),
						self.$$.insideMissedScatter
					);

					// Outside x = 276, y = 274
					var outside = _(data[1].objects)
						.map(function (d) {
							var index = _.indexBy(d.indicators, 'indicator');

							return {
								id   : d.region,
								name : regions[d.region].name,
								x    : value(index[276]),
								y    : value(index[274])
							};
						})
						.filter(function (d) {
							return util.defined(d.x) && util.defined(d.y);
						})
						.value();

					React.render(
						React.createElement(Chart, {
							type    : 'ScatterChart',
							data    : outside,
							options : options
						}),
						self.$$.outsideMissedScatter
					);

					barChart(
						self.$$.missedReasons,
						'Missed Children',
						datapoints,
						[267,268,251,264,266],
						regionMapping,
						getIndicator);

					self.missed.monitoring = formatData(
						datapoints,
						[265,273],
						regionMapping,
						getIndicator);

					self.absences.reasons = formatData(
						datapoints,
						[246,247,248,249,250],
						regionMapping,
						getIndicator);

					self.noncompliance.reasons = formatData(
						datapoints,
						[252,255,258,261,253,256,259,254,257,260,263,262],
						regionMapping,
						getIndicator);

					self.resolutions.by = formatData(
						datapoints,
						[340,341,342,343],
						regionMapping,
						getIndicator);

					self.influencers.by = formatData(
						datapoints,
						[278,279,280,281,282,283,284,285],
						regionMapping,
						getIndicator);

					self.sources.series = formatData(
						datapoints,
						[295,299,303,296,300,304,297,301,305,298,302],
						regionMapping,
						getIndicator);

				}, onError);
		}
	},

	events : {
		'point-clicked' : function (d) {
			this.$dispatch('region-selected', d.name);
		},

		'region-clicked' : function (d) {
			this.$dispatch('region-selected', d.region.name);
		}
	},

	watch : {
		'campaign' : 'fetch',
		'region'   : 'fetch'
	}
};
