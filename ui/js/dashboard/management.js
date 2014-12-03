/* global Promise */

'use strict';

var _        = require('lodash');
var moment   = require('moment');

var api      = require('../data/api');
var ratio    = require('../data/transform/ratio');
var Campaign = require('../data/model/campaign');

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
					data.objects[i].campaign = new Campaign(campaigns[data.objects[i].campaign]);
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
			.then(ratio([20, 21, 22], 55))
			.done(set('missed'));
	},
};
