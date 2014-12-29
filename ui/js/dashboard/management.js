/* global Promise */

'use strict';

var d3        = require('d3');
var _         = require('lodash');
var moment    = require('moment');

var coolgray  = require('../colors/coolgray');

var api       = require('../data/api');

var bullet    = require('../data/model/bullet');
var series    = require('../data/model/series');

var add       = require('../data/transform/add');
var color     = require('../data/transform/color');
var cumsum    = require('../data/transform/cumsum');
var each      = require('../data/transform/each');
var facet     = require('../data/transform/facet');
var map       = require('../data/transform/map');
var ratio     = require('../data/transform/ratio');
var sort      = require('../data/transform/sort');
var variables = require('../data/transform/variables');

var OFFICE = {
	1: 23,   // Nigeria
	2: 4404, // Afghanistan
	3: 128   // Pakistan
};

/**
 * Utility for generating the tickValues array for a year-to-date chart.
 *
 * Ticks will be Jan, Dec, and the current month. If the current month is either
 * Jan or Dec, then only Jan and Dec are used.
 */
function ytdTicks(month) {
	console.log(month);
	// If the current month is between March and October, the ticks should be
	// January, current month, December.
	if (month > 1 && month < 10) {
		return [1, month + 1, 12];
	}

	// If the current month is January, or February, the ticks are just the
	// current month and December.
	if (month < 2) {
		return [month + 1, 12];
	}

	// Otherwise the ticks are January and the current month
	return [1, month + 1];
}
/**
 * Utility for filling in default ranges.
 *
 * Adds a default range property to each entry in the array. A stopgap for
 * indicators not currently supporting qualitative ranges.
 */
function rangeFactory(data) {
	if (data.hasOwnProperty('ranges')) {
		return;
	}

	data.ranges = [{
		name: 'bad',
		start: 0,
		end: 0.5
	}, {
		name: 'ok',
		start: 0.5,
		end: 0.85
	}, {
		name: 'good',
		start: 0.85,
		end: 1
	}];
}

function indicators(ids, opts) {
	function emptyPromise(fulfill) {
		fulfill({
			meta: {},
			objects: []
		});
	}

	// Create a copy of the options so that we can modify the query object
	var q = _.assign({}, opts);

	if (ids instanceof Array) {
		if (ids.length === 0) {
			return new Promise(emptyPromise);
		}

		q.indicator__in = ids.join(',');
	} else {
		if (typeof ids === 'undefined' || ids === null || ids === '') {
			return new Promise(emptyPromise);
		}

		q.indicator__in = ids;
	}

	return api.datapoints(q);
}

function objects(data) {
	return data.objects || data;
}

module.exports = {
	replace : true,
	template: require('./management.html'),

	data: function () {
		return {
			offices    : [],
			campaigns  : [],
			region     : null,
			start      : new Date(),
			cases      : {
				lines: [],
				domain: [1, 12],
				xFmt : function (d) {
					return moment(d, 'M').format('MMM');
				},
				tickValues: ytdTicks
			},
			conversions: {
				lines: [],
				x    : d3.time.scale(),
				yFmt : d3.format('.0%')
			},
			capacity   : [{
				name: 'Soc. Mob. Coverage',
				indicators: []
			}, {
				name: 'IPC Skills',
				indicators: []
			}, {
				name: 'Network Size',
				indicators: [36, 35]
			}, {
				name: 'Training on Polio+',
				indicators: []
			}, {
				name: 'Local Vaccinators',
				indicators: []
			}, {
				name: 'Supervision',
				indicators: []
			}, {
				name: 'Female Vaccinators',
				indicators: [37, 38]
			}, {
				name: 'Timely Payment',
				indicators: [46, 36]
			}, {
				name: 'Female Mobilizers',
				indicators: [40, 36]
			}],
			polio     : [{
				name: 'Penta3 Coverage',
				indicators: [48, 47]
			}, {
				name: 'RI Knowledge',
				indicators: [50, 29]
			}, {
				name: 'RI Defaulters Tracking',
				indicators: []
			}, {
				name: 'Convergence Activities',
				indicators: []
			}, {
				name: 'RI No Stockouts',
				indicators: [53, 52],
			}],
			supply     : [{
				name: 'Delayed OPV Supply',
				indicators: [],
				ranges: [{
					name: 'bad',
					start: 0.5,
					end: 1
				}, {
					name: 'ok',
					start: 0.3,
					end: 0.5
				}, {
					name: 'good',
					start: 0,
					end: 0.3
				}]
			}, {
				name: 'OPV Wastage Rate',
				indicators: [],
				ranges: [{
					name: 'bad',
					start: 0.5,
					end: 1
				}, {
					name: 'ok',
					start: 0.3,
					end: 0.5
				}, {
					name: 'good',
					start: 0,
					end: 0.3
				}]
			}, {
				name: 'Cold Chain Function',
				indicators: []
			}, {
				name: 'Stock Reporting',
				indicators: []
			}],
			resources  : [{
				name: 'Funding',
				indicators: []
			}, {
				name: 'Human Resources',
				indicators: []
			}],
			microplans: []
		};
	},

	created: function () {
		var self  = this;

		// FIXME: Hack to fill out hard-coded bullet chart VMs
		this.capacity.forEach(rangeFactory);
		this.supply.forEach(rangeFactory);
		this.polio.forEach(rangeFactory);
		this.resources.forEach(rangeFactory);

		this.$on('selection-changed', function () {
			function isSelected(d) {
				return d.selected;
			}

			var office = self.offices.filter(isSelected)[0].value;
			var region = OFFICE[office];

			if (region !== self.region) {
				self.region = region;
				api.campaign({ office: office }).done(self.loadCampaigns);
			} else {
				self.loadData();
			}
		});

		api.office().done(function (data) {
			var offices = data.objects.map(function (o) {
				return {
					title   : o.name,
					value   : o.id,
					selected: false
				};
			});

			offices[0].selected = true;
			self.region = OFFICE[offices[0].value];
			self.offices = offices;

			api.campaign({ office: offices[0].value }).done(self.loadCampaigns);
		});
	},

	methods: {
		loadCampaigns: function (data) {
			this.campaigns = data.objects.map(function (o) {
				var startDate = moment(o.start_date, 'YYYY-MM-DD');

				return {
					title   : startDate.format('MMM YYYY'),
					value   : o.start_date,
					sortVal : startDate.format('YYYYMMDD'),
					selected: false
				};
			});

			this.campaigns[0].selected = true;

			this.loadData();
		},

		loadData: function () {
			// Curried function for setting a keypath on the VM that can be used as a
			// callback for when API calls complete.
			function set(keypath) {
				return function (data) {
					self.$set(keypath, data);
				};
			}

			function campaignStart(d) {
				return d.campaign.start_date;
			}

			function fetchBullets(keypath, q) {
				var section = self.$get(keypath);

				section.forEach(function (o, i) {
					if (o.indicators.length === 2) {
						indicators(o.indicators, q)
							.then(objects)
							.then(sort(campaignStart))
							.then(bullet(o.name, o.indicators[0], o.indicators[1], o.ranges))
							.done(function (data) {
								// FIXME: This is really redundant with the existing set
								// function, should just modify set to take a keypath and the
								// VM on which the keypath is set
								section.$set(i, data);
							});
					} else {
						o.value  = null;
						o.marker = null;
					}
				});
			}

			var self  = this;
			var start = moment(this.campaigns.filter(function (d) {
					return d.selected;
				})[0].value, 'YYYY-MM-DD');


			// Query parameters shared by all queries
			var q = {
				region__in    : self.region,
				campaign_start: start.clone().subtract(2, 'years').format('YYYY-MM-DD'),
				campaign_end  : start.format('YYYY-MM-DD')
			};

			this.cases.tickValues = ytdTicks(start.month());

			// Polio Cases YTD
			indicators([69, 70, 159, 160, 161, 162], q)
				.then(objects)
				.then(add([69, 70, 159, 160, 161, 162]))
				.then(facet(function (d) { return d.campaign.start_date.getFullYear(); }))
				.then(map(sort(campaignStart)))
				.then(each(cumsum(
					function (d) { return d.value; },
					function (d, v) { d.value = v; return d; }
					)))
				.then(each(variables({
					x: function (d) { return d.campaign.start_date.getMonth() + 1; },
					y: function (d) { return d.value; }
				})))
				.then(map(series(function (d) {
					return d[0].campaign.start_date.getFullYear();
				})))
				.done(set('cases.lines'));

			// Immunity Gap
			indicators([], q).done(set('immunity'));

			// Missed Children
			indicators([20, 22, 23, 24, 55], q)
				.then(objects)
				.then(sort(campaignStart))
				.then(ratio([20, 22, 23, 24], 55))
				.then(each(variables({
					x: function (d) { return d.campaign.start_date; },
					y: function (d) { return d.value; }
				})))
				.then(map(function (data) {
					// The line chart expects an array of objects with a points property
					return { points: data };
				}))
				.then(each(color(coolgray)))
				.done(set('missed'));

			// Conversions
			indicators([25, 26], q)
				.then(objects)
				.then(sort(campaignStart))
				.then(ratio(26, 25))
				.then(each(variables({
					x: function (d) { return d.campaign.start_date; },
					y: function (d) { return 1 - d.value; }
				})))
				.then(map(function (data) {
					return { points: data };
				}))
				.done(set('conversions.lines'));

			// Microplans with social data
			indicators([27, 28], q)
				.then(objects)
				.then(sort(campaignStart))
				.then(function (data) {
					if (!data || data.length < 1) {
						return [];
					}

					var d          = data[data.length - 1];
					var indicators = _.indexBy(d.indicators, 'indicator');
					var microplans = indicators[27].value;
					var socialData = indicators[28].value;

					return [{
						value: socialData,
						color: coolgray[5]
					}, {
						value: microplans - socialData,
						color: coolgray[0]
					}];
				}).done(set('microplans'));

			q.campaign_start = start.clone().subtract(4, 'months').format('YYYY-MM-DD');

			fetchBullets('capacity', q);
			fetchBullets('supply', q);
			fetchBullets('polio', q);
			fetchBullets('resources', q);
		}
	},
};
