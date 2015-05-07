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

function _fill(d) {
	return !_.isNull(d) && d.range ? this.scale(d.range) : 'transparent';
}

module.exports = {
	template : require('./district.html'),

	data : function () {
		return {
			campaign : null,
			columns  : [],
			fill     : _fill.bind(this),
			region   : null,
			regions  : {},
			series   : [],
			scale    : d3.scale.ordinal()
				.domain(['bad', 'okay', 'ok', 'good'])
				.range(['#AF373E', '#959595', '#959595','#2B8CBE'])
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

			var self = this;

			Promise.all([api.indicators({ id__in : indicators }), datapoints])
				.then(function (data) {
					var columns = _(data[0].objects)
						.reject(function (indicator) {
							return _.isEmpty(indicator.indicator_bounds);
						})
						.sortBy(function (indicator) {
							return indicators.indexOf(indicator.id);
						})
						.value();

					var bounds = _(data[0].objects)
						.indexBy('id')
						.transform(function (result, v, k) {
							result[k] = _(v.indicator_bounds)
								.map(function (bound) {
									var lower = _.isNumber(bound.mn_val) ? bound.mn_val : -Infinity;
									var upper = _.isNumber(bound.mx_val) ? bound.mx_val : Infinity;

									return _.assign({}, bound, {
										mn_val : lower,
										mx_val : upper
									});
								})
								.reject(function (bound) {
									return bound.bound_name === 'invalid';
								})
								.sortBy(function (bound) {
									switch (bound.name) {
										case 'bad':
											return 1;
										case 'ok':
										case 'okay':
											return 2;
										case 'good':
											return 3;
										default:
											return 4;
									}
								})
								.value();
						})
						.omit(function (bound, id) {
							return _.isEmpty(bound);
						})
						.value();

					console.log('bounds:', bounds);

					var data = _.map(data[1].objects, function (d) {
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
								var v = { id : name + '-' + indicator.id };
								var id = indicator.id;

								if (dataIdx[id]) {
									v.value = dataIdx[id].value

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

					self.columns = _.pluck(columns, 'short_name');
					self.series  = data;
				}, this.error);
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
		campaign : 'load',
		region   : 'load'
	}
};
