'use strict';

var moment   = require('moment');

var api      = require('../data/api');

var Dropdown = require('../component/dropdown');

/**
 * Utility for generating the tickValues array for a year-to-date chart.
 *
 * Ticks will be Jan, Dec, and the current month. If the current month is either
 * Jan or Dec, then only Jan and Dec are used.
 */
function ytdTicks(month) {
	return function (domain) {
		var lower = domain[0];
		var upper = domain[domain.length - 1];

		// If the current month is between March and October, the ticks should be
		// January, current month, December.
		if (month > lower + 1 && month < upper - 1) {
			return [lower, month, upper];
		}

		// If the current month is January, or February, the ticks are just the
		// current month and December.
		if (month <= lower + 1) {
			return [month, upper];
		}

		// Otherwise the ticks are January and the current month
		return [1, month];
	};
}

function timeTicks(domain) {
	var lower = moment(domain[0]);
	var upper = moment(domain[domain.length - 1]);
	var current = moment(upper).startOf('year');
	var ticks = [lower.toDate().getTime()];

	while (current.isAfter(lower)) {
		ticks.push(current.toDate().getTime());
		current = moment(current).subtract(1, 'year');
	}

	ticks.push(upper.toDate().getTime());

	return ticks;
}

module.exports = {

	replace : true,
	template: require('./management.html'),

	data: function () {
		return {
			region    : null,
			campaign  : null,
			campaigns : [],
			capacity  : [34, 36, 37, 40, 183, 231, 210, 226],
			polio     : [48, 50, 192, 66],
			supply    : [241, 220, 173, 197],
			resources : [169, 32],
			microplans: []
		};
	},

	attached: function () {
		var self = this;

		this._regions = new Dropdown({
			el      : '#regions',
			source  : api.regions,
			defaults: 12907, // FIXME: Hard-coded Nigeria default should be supplied by back-end based on permissions
			mapping : {
				'parent_region_id': 'parent',
				'name'            : 'title',
				'id'              : 'value'
			}
		});

		this._regions.$on('dropdown-value-changed', function (items) {
			console.debug('management::dropdown-value-changed', 'region', items);
			self.region = (items && items.length > 0) ? items[0].value : null;
		});

		this.$.campaigns.$on('dropdown-value-changed', function (items) {
			console.debug('management::dropdown-value-changed', 'campaign', items);
			self.campaign = (items && items.length > 0) ? null : items[0];
		});
	},

	methods: {

		loadCampaigns: function (data) {
			this.campaigns = data.objects.map(function (o) {
				var startDate = moment(o.start_date, 'YYYY-MM-DD');

				return {
					title   : startDate.format('MMM YYYY'),
					value   : o.start_date,
					date    : startDate.format('YYYYMMDD'),
					end     : o.end_date,
					selected: false
				};
			});

			this.campaigns[0].selected = true;
			this.campaign = this.campaigns[0];
		}

	},

	watch: {

		'region': function () {
			api.campaign({ region__in: this.region }).then(this.loadCampaigns);
			this._regions.$emit('dropdown-select', this.region);
		}

	},

	events: {
		'region-changed': function (region) {
			this.region = region;
		}
	}

};
