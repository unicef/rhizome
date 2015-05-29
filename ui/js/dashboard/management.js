'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');
var React  = require('react');

var Chart              = require('component/Chart.jsx');
var PolioCasesYtD      = require('./PolioCasesYtD.jsx');
var BulletChartSection = require('./BulletChartSection.jsx');

var api       = require('data/api');
var colors    = require('colors');
var colorUtil = require('util/color');
var format    = require('util/format');
var palette   = require('colors');
var util      = require('util/data');

var INDICATORS = {
	cases           : [168],
	immunityGap     : [431,432,433],
	missed          : [166,164,167,165],
	totalMissed     : [475],
	conversions     : [187,189],
	microplans      : [27,28],
	transitPoints   : [175,176,177,204],
	capacity        : [178,228,179,184,180,185,230,226,239],
	polio           : [245,236,192,193,191],
	supply          : [194,219,173,172],
	resources       : [169,233],
	inaccessible    : [158],
	accessPlans     : [174],
	inaccessibility : [442,443,444,445,446,447,448,449,450]
};

/**
 * Return an array with one datapoint per indicator.
 */
function melt(dataset) {
	var o = _(dataset)
		.map(function (d) {
			var base = _.omit(d, 'indicators');

			return _.map(d.indicators, function (indicator) {
				return _.assign({}, base, indicator);
			});
		})
		.flatten()
		.value();

	return o;
}

/**
 * Convert the value of each datapoint to a percentage of the total value
 */
function percentage(dataset) {
	var total = _(dataset).pluck('value').sum();

	_.forEach(dataset, function (d) {
		d.value /= total;
	});

	return dataset;
}

function seriesObject(d, ind, collection, indicators) {
	return {
		name   : indicators[ind].short_name,
		values : d
	};
}

function _microplans(data) {
	var microplans = {
		value  : null,
		domain : null,
		show   : false
	};

	if (!_.isEmpty(data)) {
		var indicators = _.indexBy(data, 'indicator');

		microplans.value  = [indicators[28]];
		microplans.domain = [0, indicators[27].value];
		microplans.show   = _(data).pluck('value').all(_.isFinite);
	}

	return microplans;
}

function _inaccessibilityBreakdown(data, indicators) {
	return _(data)
		.map(function (d) {
			// Build a new object that can be used as the VM for the table of pie
			// charts that displays the inaccessibility breakdown
			return _.assign({
				name       : indicators[d.indicator].short_name,
				value      : d3.format('.1f')(d.value * 100),
				datapoints : [{
					indicator : d.indicator,
					value     : d.value
				}]
			}, _.pick(d, 'campaign', 'region'));
		})
		.filter(function (d) {
			return _.isFinite(d.datapoints[0].value) && d.datapoints[0].value > 0;
		})
		.sortBy(_.property('datapoints[0].value'))
		.reverse()
		.value();
}

function _transitPoints(data) {
	var index = _.indexBy(data, 'indicator');

	var vaccinated = _.get(index, '[177].value');
	var inPlace    = index[175];
	var withSM     = index[176];
	var planned    = index[204];

	return {
		vaccinated : {
			value : vaccinated,
			show  : _.isFinite(vaccinated)
		},
		inPlace : {
			value  : [inPlace],
			domain : [0, _.get(planned, 'value', 1)],
			show   : _.all([inPlace, planned], _.flow(_.property('value'), _.isFinite))
		},
		withSM : {
			value  : [withSM],
			domain : [0, _.get(inPlace, 'value', 1)],
			show   : _.all([withSM, inPlace], _.flow(_.property('value'), _.isFinite))
		}
	};
}

function _immunityGap(data, indicators) {
	var immunity = _(data)
		.each(function (d) {
			// Add a property to each datapoint indicating the fiscal quarter
			d.quarter = moment(d.campaign.start_date).format('[Q]Q YYYY');
		})
		.groupBy(function (d) {
			return d.indicator + '-' + d.quarter;
		})
		.map(function (datapoints) {
			// Calculate the total number of children with X doses of OPV for
			// each quarter
			return _.assign({}, datapoints[0], {
				'value' : _(datapoints).pluck('value').sum()
			});
		})
		.groupBy('quarter')
		.map(percentage)
		.flatten()
		.reject(function (d) {
			// Exclude 4+ doses, because that is implied as 1 - <0 doses> - <1–3 doses>
			// jshint eqeqeq: false
			return d.indicator == '433';
		})
		.groupBy('indicator')
		.map(_.partialRight(seriesObject, indicators))
		.value();

		var stack = d3.layout.stack()
			.offset('zero')
			.values(function (d) { return d.values; })
			.x(function (d) { return d.campaign.start_date; })
			.y(function (d) { return d.value; });

		return stack(immunity);
}

function _missedChildren(data, indicators) {
	var missedChildren = _(data)
		.groupBy('indicator')
		.map(_.partialRight(seriesObject, indicators))
		.value();

	var stack = d3.layout.stack()
		.offset('zero')
		.values(function (d) { return d.values; })
		.x(function (d) { return d.campaign.start_date; })
		.y(function (d) { return d.value; });

	return stack(missedChildren);
}

function _conversions(data, indicators) {
	return _(data)
		.groupBy('indicator')
		.map(function (d, ind) {
			return seriesObject(
				_.sortBy(d, _.method('campaign.start_date.getTime')),
				ind,
				null,
				indicators
			);
		})
		.value();
}

module.exports = {

	template: require('./management.html'),

	data: function () {
		return {
			region          : null,
			campaign        : null,
			campaigns       : [],

			immunityGap     : [],

			capacity        : [],
			polio           : [],
			supply          : [],
			resources       : [],

			accessPlans     : [],
			inaccessibility : [],

			microplans      : {
				value  : null,
				domain : [0, 1],
				show   : false
			},

			transitPoints   : {
				vaccinated : {
					value : null,
					show  : false,
				},
				inPlace : {
					value  : [],
					domain : [0, 1],
					show   : false
				},
				withSM : {
					value  : [],
					domain : [0, 1],
					show   : false
				}
			}
		};
	},

	created : function () {
		// Prefetch all the indicator definitions we're going to need and index
		// them by ID
		this._indicators = api.indicators({ id__in : _(INDICATORS).values().flatten().value() })
			.then(
				function (data) {
					return _.indexBy(data.objects, 'id');
				},
				function () {
					console.error('Failed to fetch indicators for Management Dashboard');
					debugger;
				});
	},

	computed: {
		campaignName: function () {
			return moment(this.campaign.end, 'YYYY-MM-DD').format('MMM YYYY');
		}
	},

	methods: {
		fetch: function () {
			if (!this.region || !this.campaign) {
				return;
			}

			var self  = this;
			var start = moment(this.campaign.start_date);

			var meltObjects  = _.flow(_.property('objects'), melt);

			// Polio cases
			var q = {
				indicator__in  : INDICATORS.cases,
				region__in     : this.region.id,
				campaign_start : start.clone().startOf('year').subtract(2, 'years').format('YYYY-MM-DD'),
				campaign_end   : moment(this.campaign.end_date).format('YYYY-MM-DD')
			};

			api.datapoints(q)
				.then(meltObjects)
				.then(function (data) {
					var ytd = React.createElement(PolioCasesYtD, {
						campaign : self.campaign,
						data     : data,
						region   : self.region
					});

					React.render(ytd, self.$$.polioCases);
				});

			// Fetch data for current campaign for pie charts
			q.indicator__in = _(INDICATORS)
				.pick('inaccessibility', 'accessPlans', 'transitPoints', 'microplans')
				.values()
				.flatten()
				.value();

			q.campaign_start = start.format('YYYY-MM-DD');

			Promise.all([api.datapoints(q).then(meltObjects), this._indicators])
				.then(_.spread(function (data, indicators) {
					var microplans = _.filter(data, function (d) {
						return _.includes(INDICATORS.microplans, Number(d.indicator));
					});

					var inaccessibility = _.filter(data, function (d) {
						return _.includes(INDICATORS.inaccessibility, Number(d.indicator));
					});

					var transitPoints = _.filter(data, function (d) {
						return _.includes(INDICATORS.transitPoints, Number(d.indicator));
					});

					self.microplans = _microplans(microplans);

					self.inaccessibility = _inaccessibilityBreakdown(
						inaccessibility, indicators);

					self.accessPlans = _(data).filter(function (d) {
							return _.includes(INDICATORS.accessPlans, Number(d.indicator));
						});

					self.transitPoints = _transitPoints(transitPoints);
				}));

			// Fetch the immunity gap data
			q.indicator__in  = INDICATORS.immunityGap;
			q.campaign_start = start.clone()
				.startOf('quarter')
				.subtract(3, 'years')
				.format('YYYY-MM-DD');

			Promise.all([api.datapoints(q).then(meltObjects), this._indicators])
				.then(_.spread(function (data, indicators) {
					var immunityGap = _immunityGap(data, indicators);

					var lower = start.clone()
						.startOf('quarter')
						.subtract(3, 'years');
					var upper = start.clone().endOf('quarter');

					var immunityScale = _.map(d3.time.scale()
							.domain([lower.valueOf(), upper.valueOf()])
							.ticks(d3.time.month, 3),
						_.method('getTime')
					);

					React.render(
						React.createElement(
							Chart,
							{
								data    : immunityGap,
								type    : 'ColumnChart',
								options : {
									aspect  : 1.609,
									color   : _.flow(
										_.property('name'),
										d3.scale.ordinal().domain(_.pluck('name', immunityGap)).range(palette)
									),
									domain  : _.constant(immunityScale),
									values  : _.property('values'),
									x       : function (d) { return moment(d.campaign.start_date).startOf('quarter').valueOf(); },
									xFormat : function (d) { return moment(d).format('[Q]Q [’]YY'); },
									y0      : _.property('y0'),
									yFormat : d3.format('%')
								}
							}
						),
						self.$$.immunityGap
					);
				}));

			q.indicator__in  = _(INDICATORS)
				.pick('missed', 'conversions', 'inaccessible')
				.values()
				.flatten()
				.value();

			q.campaign_start = start.clone()
				.startOf('month')
				.subtract(1, 'year')
				.format('YYYY-MM-DD');

			// Build the line charts
			Promise.all([api.datapoints(q).then(meltObjects), this._indicators])
				.then(_.spread(function (data, indicators) {
					var missed = _.filter(data, function (d) {
						return _.includes(INDICATORS.missed, Number(d.indicator));
					});

					var conversions = _.filter(data, function (d) {
							return _.includes(INDICATORS.conversions, Number(d.indicator));
						});

					var inaccessible = _.filter(data, function (d) {
						return _.includes(INDICATORS.inaccessible, Number(d.indicator));
					});

					var lower = start.clone().startOf('month').subtract(1, 'year');
					var upper = start.clone().endOf('month');

					var missedScale = _.map(d3.time.scale()
							.domain([lower.valueOf(), upper.valueOf()])
							.ticks(d3.time.month, 1),
						_.method('getTime')
					);

					var missedChildren = _missedChildren(missed, indicators);

					React.render(
						React.createElement(Chart, {
							data    : missedChildren,
							type    : 'ColumnChart',
							options : {
								aspect  : 1.909344491,
								color   : _.flow(
									_.property('name'),
									d3.scale.ordinal().domain(_.pluck('name', missedChildren)).range(palette)
								),
								domain  : _.constant(missedScale),
								values  : _.property('values'),
								x       : function (d) { return moment(d.campaign.start_date).startOf('month').toDate().getTime(); },
								xFormat : function (d) { return moment(d).format('MMM YYYY'); },
								y0      : _.property('y0'),
								yFormat : d3.format('%'),
							}
						}),
						self.$$.missedChildren
					);

					React.render(
						React.createElement(Chart, {
							type    : 'LineChart',
							data    : _conversions(conversions, indicators),
							id      : 'conversions',
							options : {
								domain  : _.constant([lower.toDate(), upper.toDate()]),
								values  : _.property('values'),
								x       : _.property('campaign.start_date'),
								y       : _.property('value'),
								yFormat : d3.format('%'),
								aspect  : 2.260237781
							}
						}),
						self.$$.conversions
					);
                    console.log(inaccessible,indicators);
					React.render(
						React.createElement(Chart, {
							type    : 'LineChart',
							data    : _conversions(inaccessible, indicators),
							id      : 'inaccessible-children',
							options : {
								aspect  : 2.664831804,
								domain  : _.constant([lower.toDate(), upper.toDate()]),
								values  : _.property('values'),
								x       : _.property('campaign.start_date'),
								y       : _.property('value'),
								yFormat : d3.format(',.0f')
							}
						}),
						self.$$.inaccessible
					);

				}));

			// Build the map
			Promise.all([
					api.datapoints({
						indicator__in     : INDICATORS.totalMissed,
						parent_region__in : this.region.id,
						campaign_start    : start.format('YYYY-MM-DD'),
						campaign_end      : moment(this.campaign.end_date).format('YYYY-MM-DD')
					}).then(meltObjects),
					api.geo({ parent_region__in : [this.region.id] }),
					api.datapoints({
						indicator__in  : INDICATORS.totalMissed,
						region__in     : this.region.id,
						campaign_start : start.format('YYYY-MM-DD'),
						campaign_end   : moment(this.campaign.end_date).format('YYYY-MM-DD')
					}).then(meltObjects),

					api.geo({ region__in : [this.region.id] })
				])
				.then(_.spread(function (data, regions, natl, border) {
					var index = _(data)
						.filter(function (d) {
							return _.isEqual(d.campaign.start_date, self.campaign.start_date);
						})
						.indexBy('region')
						.value();

					var missed = _.map(regions.objects.features, function (feature) {
							var region = _.get(index, feature.properties.region_id);

							return _.merge({}, feature, {
									properties : { value : _.get(region, 'value') }
								});
						});

					border.objects.features[0].properties.value = natl[0].value;

					var props = {
						type    : 'ChoroplethMap',
						data    : missed,
						options : {
							domain  : _.constant([0, 0.1]),
							border  : border.objects.features,
							onClick : function (d) {
								if (self.regions.hasOwnProperty(d.properties.region_id)) {
									self.$dispatch('region-selected',
										self.regions[d.properties.region_id].name);
								}
							},
							onMouseOver : function (d, el) {
								if (self.regions.hasOwnProperty(d.properties.region_id)) {
									var evt = d3.event;
									self.$dispatch('tooltip-show', {
										el       : el,
										position : {
											x : evt.pageX,
											y : evt.pageY
										},
										data : {
											text     : self.regions[d.properties.region_id].name,
											template : 'tooltip-default'
										}
									});
								}
							},
							onMouseOut : function (d, el) {

								self.$dispatch('tooltip-hide', { el : el });
							}
						}
					};

					React.render(
						React.createElement(Chart, props),
						self.$$.missedChildrenMap
					);
				}));

			// Bullet charts
			q.indicator__in = _(INDICATORS)
				.pick('capacity', 'polio', 'supply', 'resources')
				.values()
				.flatten()
				.value();

			q.campaign_start = start.clone()
				.subtract(4, 'months')
				.format('YYYY-MM-DD');

			var bullets = api.datapoints(q)
				.then(meltObjects)
				.then(_.partial(_.groupBy, _, 'indicator'));

			Promise.all([bullets, this._indicators])
				.then(_.spread(function (data, indicators) {

					var fillBulletChart = function (id) {
						var dataset = _.get(data, id, [{
							campaign : self.campaign,
							value    : null,
							region   : null
						}]);

						return _.map(dataset, function (d) {
							return _.assign({}, d, { indicator : _.get(indicators, id) });
						});
					};

					var attachBulletChart = function (el, data, cols) {
						React.render(
							React.createElement(
								BulletChartSection,
								{
									campaign : self.campaign,
									cols     : _.isFinite(cols) ? cols : 1,
									data     : data,
									showHelp : self.showBulletTooltip,
									hideHelp : self.hideTooltip
								}
							),
							el
						);
					}
					attachBulletChart(
						self.$$.capacity,
						_(INDICATORS.capacity).map(fillBulletChart).flatten().value(),
						2
					);

					attachBulletChart(
						self.$$.supply,
						_(INDICATORS.supply).map(fillBulletChart).flatten().value()
					);

					attachBulletChart(
						self.$$.polio,
						_(INDICATORS.polio).map(fillBulletChart).flatten().value()
					);

					attachBulletChart(
						self.$$.resources,
						_(INDICATORS.resources).map(fillBulletChart).flatten().value()
					);
				}));
		},

		showBulletTooltip : function (indicator, evt) {
			this.$dispatch('tooltip-show', {
				el   : evt.target,
				data : _.assign({},
					indicator,
					{ template : 'tooltip-indicator' })
			});
		},

		hideTooltip : function (evt) {
			this.$dispatch('tooltip-hide', {
				el : evt.target,
			});
		}
	},

	watch: {
		'campaign' : 'fetch',
		'region'   : 'fetch'
	}
};
