/* global window */
'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');
var React  = require('react');

var api  = require('data/api');
var util = require('util/data');

var HeatMap = require('component/chart/heatmap.jsx');

var RANGE_ORDER = {
	'bad'  : 0,
	'ok'   : 1,
	'okay' : 1,
	'good' : 2
};

/**
 * @private
 * Return true if indicator is an object with an array of indicator_bounds.
 */
function _hasBounds(indicator) {
	return _.isObject(indicator) && !_.isEmpty(indicator.indicator_bounds);
}

/**
 * @private
 * Return an array of indicator objects sorted by order.
 *
 * @param {Object} indicators Response object from indicators API
 * @param {Array} order An array of indicator IDs that defines the order of
 *   the returned array
 */
function _heatmapColumns(indicators, order) {
	return _(indicators.objects)
		.filter(_hasBounds)
		.sortBy(function (indicator) {
			return order.indexOf(indicator.id);
		})
		.value();
}

/**
 * @private
 * Convert "NULL" strings on a bound definition to +/- Infinity
 *
 * Create a new object with non-number properties replaced by +/- Infinity.
 * mn_val is replaced by -Infinity, and mx_val is replaced by Infinity, if
 * either has a non-numeric property.
 *
 * @param {Object} bound A target range definition for an indicator
 */
function _openBounds(bound) {
	var lower = _.isNumber(bound.mn_val) ? bound.mn_val : -Infinity;
	var upper = _.isNumber(bound.mx_val) ? bound.mx_val : Infinity;

	return _.assign({}, bound, {
		mn_val : lower,
		mx_val : upper
	});
}

function _getBoundOrder(bound) {
	return _.get(RANGE_ORDER, bound.bound_name, Infinity);
}


module.exports = {
	template : require('./district.html'),

	data : function () {
		return {
			campaign : null,
			columns  : [],
			region   : null,
			regions  : {},
			series   : [],
			showEmpty: false,
		};
	},

	methods : {
		error : function () {
			// FIXME
			window.alert('Dammit!');
		},

		load : function () {
			this.loading = true;

			if (!(this.campaign && this.region)) {
				return;
			}

			var indicators = [
				475,166,164,167,165, // Missed Children
				222, // Microplans
				187,189, // Conversions
				// FIXME: Transit points in place and with SM
				178,228,179,184,180,185,230,226,239, // Capacity to Perform
				194,219,173,172, // Supply
				245,236,192,193,191, // Polio+
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

			var columns = api.indicators({ id__in : indicators })
				.then(_.partialRight(_heatmapColumns, indicators));

			var self = this;

			Promise.all([columns, datapoints])
				.then(function (data) {
					var columns = data[0];

					// Create a function for extracting and formatting target value ranges
					// from the indicator definitions.
					var getTargetRanges = _.flow(
						_.property('indicator_bounds'), // Extract bounds definition
						_.partial(_.reject, _, { bound_name: 'invalid' }), // Filter out the 'invalid' target ranges
						_.partial(_.map, _, _openBounds), // Replace 'NULL' with +/- Infinity
						_.partial(_.sortBy, _, _getBoundOrder) // Sort the bounds: bad, ok/okay, good
					);

					var bounds = _(columns)
						.indexBy('id')
						.mapValues(getTargetRanges)
						.omit(_.isEmpty)
						.value();

					var series = _.map(data[1].objects, function (d) {
						var dataIdx = _.indexBy(d.indicators, 'indicator');
						var name    = d.region;

						if (self.regions[name]) {
							name = self.regions[name];
						}

						if (name.name) {
							name = name.name;
						}

						return {
							id     : name,
							name   : name,
							values : _.map(columns, function (indicator) {
								var v = {
									id        : name + '-' + indicator.id,
									indicator : indicator.id
								};

								var id = indicator.id;

								if (dataIdx[id]) {
									v.value = dataIdx[id].value;

									if (util.defined(v.value)) {
										_.each(bounds[id], function (bound) {
											if (v.value >= bound.mn_val && v.value <= bound.mx_val) {
												v.range = bound.bound_name;
											}
										});
									}
								}

								return v;
							})
						};
					});

					self.columns = columns;
					self.series  = series;
				}, this.error);
		},

		render : function () {
			var valueDefined = _.partial(util.defined, _, function (d) { return d.value; });
			var notEmpty     = _.partial(_.some, _, valueDefined);

			var visible = _(this.series)
				.pluck('values')
				.flatten()
				.groupBy('indicator')
				.mapValues(this.showEmpty ? _.constant(true) : notEmpty)
				.value();

			var props = {};

			props.headers = _(this.columns)
				.filter(_.flow(_.property('id'), _.propertyOf(visible)))
				.pluck('short_name')
				.value();

			// Returns new series objects where the values property contains only
			// objects for indicators that are visible
			var filterInvisibleIndicators = function (s) {
				return _.assign({}, s, {
					values : _.filter(s.values, _.flow(_.property('indicator'), _.propertyOf(visible)))
				});
			};

			props.series = _.map(this.series, filterInvisibleIndicators);

			props.scale = d3.scale.ordinal()
					.domain(['bad', 'okay', 'ok', 'good'])
					.range(['#AF373E', '#959595', '#959595','#2B8CBE']);

			var heatmap = React.createElement(HeatMap, props, null);
			React.render(heatmap, this.$$.heatmap, null);
		}
	},

	filters : {
		jump : function (value) {
			var parent = this.$parent;

			while (parent && !parent.campaign) {
				parent = parent.$parent;
			}

			if (!(parent.campaign && parent.campaign.start_date)) {
				return null;
			}

			return '/datapoints/management-dashboard/' + value + '/' +
				moment(parent.campaign.start_date).format('YYYY/MM');
		}
	},

	watch : {
		'campaign'  : 'load',
		'columns'   : 'render',
		'region'    : 'load',
		'series'    : 'render',
		'showEmpty' : 'render'
	}
};
