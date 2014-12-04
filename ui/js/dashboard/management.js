/* global Promise */

'use strict';

var _        = require('lodash');
var moment   = require('moment');

var api      = require('../data/api');
var ratio    = require('../data/transform/ratio');
var sort     = require('../data/transform/sort');
var campaign = require('../data/model/campaign');
var bullet   = require('../data/model/bullet');

/**
 * Utility for filling in default ranges.
 *
 * Adds a default range property to each entry in the array. A stopgap for
 * indicators not currently supporting qualitative ranges.
 */
function rangeFactory(data) {
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
	// Create a copy of the options so that we can modify the query object
	var q = _.assign({}, opts);

	if (ids instanceof Array) {
		q.indicator__in = ids;
	} else {
		q.indicator = ids;
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
		return {};
	},

	created: function () {
		// Curried function for setting a keypath on the VM that can be used as a
		// callback for when API calls complete.
		function set(keypath) {
			return function (data) {
				self.$set(keypath, data);
			};
		}

		function add(keypath) {
			return function (data) {
				var arr = self.$get(keypath);

				if (!arr) {
					arr = [];
					self.$set(keypath, arr);
				}

				arr.push(data);
			};
		}

		function campaignStart(d) {
			return d.campaign.start_date;
		}

		var self  = this;
		var start = (this.start ? moment(this.start) : moment()).subtract(2, 'years').format('YYYY-MM-DD');

		// Query parameters shared by all queries
		var q = {
			region        : this.region,
			campaign_start: start
		};

		indicators(1, q).done(set('cases'));

		indicators([], q).done(set('immunity'));

		indicators([20, 21, 22, 55], q)
			.then(sort(campaignStart))
			.then(ratio([20, 21, 22], 55))
			.done(set('missed'));

		q.campaign_start = (this.start ?
			moment(this.start) :
			moment()).subtract(4, 'months').format('YYYY-MM-DD');

		var capacity = [{
			name: 'Soc. Mob. Coverage',
			indicators: [34, 33]
		}, {
			name: 'Network Size',
			indicators: [36, 35]
		}, {
			name: 'Female mobilizers',
			indicators: [40, 36]
		}];

		capacity.forEach(rangeFactory);

		for (var i = capacity.length - 1; i >= 0; --i) {
			var ind = capacity[i];

			indicators(ind.indicators, q)
				.then(sort(campaignStart))
				.then(bullet(ind.name, ind.indicators[0], ind.indicators[1], ind.ranges))
				.done(add('capacity'));
		}
	},
};
