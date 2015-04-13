'use strict';

var _     = require('lodash');
var Store = require('./Store');

var _dashboards = [{
		'name' : 'Campaign Performance',
		'slug' : 'campaign-performance',
	}, {
		'name'   : 'Independent Monitoring',
		'slug'   : 'independent-monitoring',
		'region' : 'Nigeria'
	}];

var _index = _.indexBy(_dashboards, 'slug');

var DashboardStore = _.assign({}, Store, {
	/**
	 * Return an array of all available dashboard definitions.
	 */
	getAll : function () {
		return _dashboards;
	},

	/**
	 * Return the definition for a dashboard's slug or undefined.
	 */
	get : function (slug) {
		return _index[slug];
	}
});

module.exports = DashboardStore;
