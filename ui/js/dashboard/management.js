'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var api    = require('data/api');
var util   = require('util/data');

var INDICATORS = {
	cases           : [168],
	immunityGap     : [431,432,433],
	missed          : [166,164,167,165],
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

function _polioCases(data, campaign) {
	var cases = _(data)
		.groupBy(_.method('campaign.start_date.getFullYear'))
		.map(function (cases, year) {
			// Aggregate polio cases by year
			return {
				name   : year,
				values : _(cases)
					.groupBy(_.method('campaign.start_date.getMonth'))
					.map(function (d, month) {
						// Aggregate polio cases by month within each year
						return {
							month : month,
							value : _(d).pluck('value').sum()
						};
					})
					.sortBy('month')
					.map(function (d, i, arr) {
						// Set the 'date' property on all objects to whatever month is
						// correct but for the current year. This is a hack so that the line
						// chart will render the lines by month, instead of sequentially
						return {
							month      : d.month,
							year       : year,
							date       : moment({ M: d.month }).toDate(),
							newCases   : d.value,
							totalCases : _(arr).take(i + 1).pluck('value').sum()
						};
					})
					.value()
			};
		})
		.sortBy('name')
		.value();

	var thisYear  = campaign.start_date.getFullYear();
	var thisMonth = campaign.start_date.getMonth();
	var latest    = _.find(cases, function (d) { return d.name == campaign.start_date.getFullYear(); });

	// Fill in missing value for current campaign
	if (_.isUndefined(latest)) {
		latest = {
			name : thisYear,
			values : [{
				month      : 0,
				year       : thisYear,
				newCases   : 0,
				totalCases : 0
			}]
		};

		cases.push(latest);
	}

	var currentCampaign = _.find(latest.values, function (d) { return d.month === thisMonth; });

	if (_.isUndefined(currentCampaign)) {
		currentCampaign = _.assign({}, _.last(latest.values), {
			month    : thisMonth,
			newCases : 0
		});

		latest.values.push(currentCampaign);
	}

	return {
		cases      : cases,
		totalCases : currentCampaign.totalCases,
		newCases   : currentCampaign.newCases
	};
}

function _microplans(data) {
	var microplans = {
		value  : null,
		domain : null,
		show   : false
	};

	if (!_.isEmpty(data)) {
		var indicators = _.indexBy(data.indicators, 'indicator');

		microplans.value  = [indicators[28]];
		microplans.domain = [0, indicators[27].value];
		microplans.show   = _(data).pluck('value').all(_.isFinite);
	}

	return microplans;
}

function _inaccessibilityBreakdown(data, indicators) {
	return _(data)
		.thru(melt)
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
			return _.isFinite(d.datapoints[0].value);
		})
		.sortBy(_.property('datapoints[0].value'))
		.value();
}

function _transitPoints(data) {
	var index = _.indexBy(data, 'indicator');

	var vaccinated = _.get(index, '[177].value');
	var inPlace    = _.get(index, '[175].value');
	var withSM     = _.get(index, '[176].value');
	var planned    = _.get(index, '[204].value');

	return {
		vaccinated : {
			value : vaccinated,
			show  : _.isFinite(vaccinated)
		},
		inPlace : {
			value  : [inPlace],
			domain : [0, planned],
			show   : _.all([inPlace, planned], _.isFinite)
		},
		withSM : {
			value  : [withSM],
			domain : [0, inPlace],
			show   : _.all([withSM, inPlace], _.isFinite)
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

			cases : {
				series     : [],
				totalCases : null,
				newCases   : null
			},

			immunityGap     : [],
			missedChildren  : [],
			conversions     : [],

			capacity        : [],
			polio           : [],
			supply          : [],
			resources       : [],

			inaccessible    : [],
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

			var q = {
				indicator__in  : INDICATORS.cases,
				region__in     : this.region.id,
				campaign_start : start.clone().startOf('year').subtract(2, 'years').format('YYYY-MM-DD'),
				campaign_end   : moment(this.campaign.end_date).format('YYYY-MM-DD')
			};

			api.datapoints(q)
				.then(meltObjects)
				.then(function (data) {
					self.cases = _polioCases(data, self.campaign);
				});

			// Fetch data for current campaign for pie charts
			api.datapoints({
					indicator__in  : _(INDICATORS).pick('inaccessibility', 'accessPlans', 'transitPoints').values().flatten().value(),
					region__in     : this.region.id,
					campaign__in   : this.campaign.id
				})
				.then(meltObjects)
				.then(function (data) {
					var microplans = _.filter(data, function (d) {
						return _.includes(INDICATORS.microplans, d.indicator);
					});

					var inaccessibility = _.filter(data, function (d) {
						return _.includes(INDICATORS.inaccessibility, d.indicator);
					});

					var transitPoints = _.filter(data, function (d) {
						return _.includes(INDICATORS.transitPoints, d.indicator);
					});

					self.microplans = _microplans(microplans);

					self.inaccessibility = _inaccessibilityBreakdown(
						inaccessibility,
						self._indicators);

					self.accessPlans = _(data).filter(function (d) {
							return _.includes(INDICATORS.accessPlans, d.indicator);
						})
						.pluck('value')
						.first();

					self.transitPoints = _transitPoints(transitPoints);
				});

			// Fetch the immunity gap data
			q.indicator__in  = INDICATORS.immunityGap;
			q.campaign_start = start.clone()
				.startOf('month')
				.subtract(3, 'years')
				.format('YYYY-MM-DD');

			Promise.all([api.datapoints(q).then(meltObjects), this._indicators])
				.then(_.spread(function (data, indicators) {
					self.immunityGap = _immunityGap(data, indicators);
				}));

			q.indicator__in  = _(INDICATORS).pick('missed', 'conversions').values().flatten().value();
			q.campaign_start = start.clone()
				.startOf('month')
				.subtract(1, 'year')
				.format('YYYY-MM-DD');

			Promise.all([api.datapoints(q).then(meltObjects), this._indicators])
				.then(_.spread(function (data, indicators) {
					var missed = _.filter(data, function (d) {
						return _.includes(INDICATORS.missed, d.indicator);
					});

					var conversions = _.filter(data, function (d) {
						return _.includes(INDICATORS.conversions, d.indicator);
					});

					self.missedChildren = _missedChildren(missed, indicators);
					self.conversions    = _conversions(conversions, indicators);
				}));

			// Bullet charts
			q.indicator__in = _(INDICATORS).pick('capacity', 'polio', 'supply', 'resources').values().flatten().value();
			q.campaign_start = start.clone()
				.subtract(4, 'months')
				.format('YYYY-MM-DD');

			var bullets = api.datapoints(q)
				.then(meltObjects)
				.then(function (data) {
					return _(data).groupBy('indicator');
				});

			Promise.all([bullets, this._indicators])
				.then(_.spread(function (data, indicators) {
					var series = _.partialRight(seriesObject, indicators);

					self.capacity  = data.pick(INDICATORS.capacity).map(series).value();
					self.polio     = data.pick(INDICATORS.polio).map(series).value();
					self.supply    = data.pick(INDICATORS.supply).map(series).value();
					self.resources = data.pick(INDICATORS.resources).map(series).value();
				}));
		},
	},

	watch: {
		'campaign' : 'fetch',
		'region'   : 'fetch'
	}
};
