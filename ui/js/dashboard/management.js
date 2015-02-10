'use strict';

var moment   = require('moment');

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

	template: require('./management.html'),

	data: function () {
		return {
			region    : null,
			regionName: '',
			campaign  : null,
			campaigns : [],
			capacity  : [178,228,179,184,180,185,230,226,239],
			polio     : [236,192,193,191],
			supply    : [194,219,173,172],
			resources : [169,233],
			microplans: []
		};
	},

	computed: {
		campaignName: function () {
			return moment(this.campaign.start_date).format('MMM YYYY');
		}
	}
};
