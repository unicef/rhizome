/* global Promise */

'use strict';

var _        = require('lodash');
var moment   = require('moment');

var api      = require('../data/api');
var ratio    = require('../data/transform/ratio');
var sort     = require('../data/transform/sort');
var campaign = require('../data/model/campaign');
var bullet   = require('../data/model/bullet');

// FIXME: Hard-coded mapping from office ID to region ID for countries because
// region_type currently doesn't distinguish states and countries.
var OFFICE = {
	1: 23,   // Nigeria
	2: 4404, // Afghanistan
	3: 128   // Pakistan
};

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

	// Return a promise so we can chain the requests for datapoints with the
	// campaign lookups.
	return new Promise(function (fulfill) {

		// Fetch datapoints first, then look up the campaigns. Once campaign data
		// has been filled in, fulfill the promise.

		api.datapoints(q).done(function (data) {
			var campaigns = data.objects.map(function (d) { return d.campaign; });

			api.campaign({
				id__in: campaigns
			}).done(function (campaignData) {
				var campaigns = _.indexBy(campaignData.objects, 'id');

				// Replace the campaign IDs with campaign objects
				for (var i = data.objects.length - 1; i >= 0; --i) {
					data.objects[i].campaign = campaign(campaigns[data.objects[i].campaign]);
				}

				fulfill(data);
			});
		});
	});
}

module.exports = {
	replace : true,
	template: require('./management.html'),

	data: function () {
		return {
			offices    : [],
			region     : null,
			start      : new Date(),
			conversions: [],
			capacity   : [{
				name: 'Soc. Mob. Coverage',
				indicators: [34, 35]
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
			supply     : [{
				name: 'DPT3 Coverage',
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
				name: 'RI Stockouts',
				indicators: [66, 65],
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
			}],
			polio      : [{
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
			}]
		};
	},

	created: function () {
		var self  = this;

		// FIXME: Hack to fill out hard-coded bullet chart VMs
		this.capacity.forEach(rangeFactory);
		this.supply.forEach(rangeFactory);
		this.polio.forEach(rangeFactory);
		this.resources.forEach(rangeFactory);

		this.$on('selection-changed', function (data) {
			self.region = OFFICE[data.selected.value];
			self.loadData();
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
			self.loadData();
		});
	},

	methods: {
		loadData: function () {
			console.log('loadData');
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
							.then(sort(campaignStart))
							.then(bullet(o.name, o.indicators[0], o.indicators[1], o.ranges))
							.done(set(keypath + '[' + i + ']'));
					}
				});
			}

			var self  = this;
			var start = (this.start ? moment(this.start) : moment()).subtract(2, 'years').format('YYYY-MM-DD');

			// Query parameters shared by all queries
			var q = {
				parent_region : self.region,
				campaign_start: start
			};

			indicators(1, q).done(set('cases'));

			indicators([], q).done(set('immunity'));

			indicators([20, 21, 22, 55], q)
				.then(sort(campaignStart))
				.then(ratio([20, 21, 22], 55))
				.done(set('missed'));

			indicators([25, 26], q)
				.then(sort(campaignStart))
				.then(ratio(25, 26))
				.done(set('conversions'));

			q.campaign_start = (self.start ?
				moment(self.start) :
				moment()).subtract(4, 'months').format('YYYY-MM-DD');

			fetchBullets('capacity', q);
			fetchBullets('supply', q);
			fetchBullets('polio', q);
			fetchBullets('resources', q);
		}
	},
};
