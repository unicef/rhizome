'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var api    = require('data/api');
var util   = require('util/data');

module.exports = {

	template: require('./management.html'),

	data: function () {
		return {
			region          : null,
			campaign        : null,
			campaigns       : [],
			immunity        : [],
			capacity        : [178,228,179,184,180,185,230,226,239],
			polio           : [245,236,192,193,191],
			supply          : [194,219,173,172],
			resources       : [169,233],
			inaccessibility : [],
			microplans      : [],
			cases           : null,
			newCases        : null,
			transitPoints   : {
				showVaccinated : false,
				showInPlace    : false,
				showWithSM     : false,
				vaccinated     : null,
				planned        : null,
				inPlace        : null,
				withSM         : null,
				pctInplace     : [],
				pctWithSM      : []
			}
		};
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

			// Fetch polio cases data for this year to display over the polio cases
			// line chart
			var start = moment(this.campaign.start_date).startOf('year');
			var q     = {
				indicator__in  : 168,
				region__in     : [this.region.id],
				campaign_start : start.format('YYYY-MM-DD'),
				campaign_end   : moment(this.campaign.end_date).format('YYYY-MM-DD')
			};

			var self = this;

			api.datapoints(q)
				.then(function (data) {
					var cases = data.objects.map(function (obj) {
							var datapoint  = _.pick(obj, 'campaign', 'region');
							var indicators = _.indexBy(obj.indicators, 'indicator');

							datapoint.value = indicators['168'].value;

							return datapoint;
						});

					var campaigns = _.indexBy(cases, function (c) {
						return moment(c.campaign.start_date).format('YYYYMMDD');
					});

					if (campaigns.hasOwnProperty(self.campaign.date)) {
						self.newCases = campaigns[self.campaign.date].value;
					} else {
						self.newCases = null;
					}

					self.cases = _.reduce(cases, function (sum, c) {
						return sum + c.value;
					}, 0);
				});

			// Fetch inaccesibility data for this campaign
			var inaccessibility = [442,443,444,445,446,447,448,449,450];

			q = {
				indicator__in  : inaccessibility,
				region__in     : [this.region.id],
				campaign_start : moment(this.campaign.start_date).startOf('month').format('YYYY-MM-DD'),
				campaign_end   : moment(this.campaign.end_date).format('YYYY-MM-DD')
			};

			Promise.all([api.indicators({ id__in: inaccessibility }), api.datapoints(q)])
				.then(function (results) {
					var index      = _.indexBy(results[0].objects, 'id');
					var data       = results[1];
					var objects    = data.objects;
					var indicators = {};

					objects.forEach(function (o) {
						o.indicators.forEach(function (d) {
							indicators[d.indicator] = _.assign({
								name           : index[d.indicator].short_name,
								value          : d3.format('.1f')(d.value * 100),
								hiddenForPrint : d.value === 0,
								datapoints     : [{
									indicator : d.indicator,
									value     : d.value
								}]
							}, _.pick(o, 'campaign', 'region'));
						});
					});

					self.inaccessibility = _(indicators)
						.values()
						.sortBy(function (d) {
							return d.datapoints[0].value;
						})
						.reverse()
						.value();
				});

			// Fetch transit points
			q.indicator__in = [175,176,177,204];
			q.region__in    = [this.region.id];

			api.datapoints(q)
				.then(function (data) {
					if (data.objects.length > 1) {
						console.warn('Multiple campaigns or regions returned, expected one');
					}

					var indicators = data.objects[0].indicators;

					for (var i = indicators.length - 1; i >= 0; i--) {
						var d = indicators[i];

						switch(d.indicator) {
							case '175':
								self.transitPoints.inPlace     = d.value;
								break;

							case '176':
								self.transitPoints.withSM     = d.value;
								break;

							case '177':
								self.transitPoints.vaccinated     = d.value;
								self.transitPoints.showVaccinated = util.defined(d.value);
								break;

							case '204':
								self.transitPoints.planned = d.value;
								break;

							default:
								break;
						}
					}
					var hasPlanned                 = util.defined(self.transitPoints.planned);
					self.transitPoints.showInPlace = util.defined(self.transitPoints.inPlace) && hasPlanned;
					self.transitPoints.showWithSM  = util.defined(self.transitPoints.withSM) && hasPlanned;

					self.transitPoints.pctInplace = [{
						indicator : 'Transit Points in Place',
						value     : self.transitPoints.inPlace / self.transitPoints.planned
					}];

					self.transitPoints.pctWithSM  = [{
						indicator : 'Transit Points with SM',
						value     : self.transitPoints.withSM / self.transitPoints.inPlace
					}];
				});

			// Fetch the immunity gap data
			q.indicator__in  = [431,432];
			q.campaign_start = moment(this.campaign.start_date)
				.startOf('month')
				.subtract(3, 'years')
				.format('YYYY-MM-DD');

			api.datapoints(q)
				.then(function (data) {
					var immunity = _(data.objects)
						.reject(function (d) {
							return _.every(d.indicators, function (ind) {
								return _.isNull(ind.value) || _.isUndefined(ind.value);
							});
						})
						.map(function (d) {
							// Separate out the (indicator, value) pairs from each datapoint's
							// indicators array so that we have an array of datapoints, each
							// representing only one indicator with one value
							var base = _.omit(d, 'indicators');

							// Add a property to each datapoint indicating the fiscal quarter
							base.quarter = moment(d.campaign.start_date).format('[Q]Q YYYY');

							return _.map(d.indicators, function (indicator) {
								return _.assign({}, base, indicator);
							});
						})
						.flatten()
						.groupBy(function (d) {
							return d.indicator + '-' + d.quarter;
						})
						.map(function (datapoints) {
							var mean = _(datapoints).pluck('value').sum() / datapoints.length;

							return _.assign({}, _.omit(datapoints[0], 'value'), {
								'value' : mean
							});
						})
						.value();

						self.immunity = immunity;
				});
		},
	},

	watch: {
		'campaign' : 'fetch',
		'region'   : 'fetch'
	}
};
