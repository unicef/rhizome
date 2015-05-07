'use strict';

var _     = require('lodash');
var Store = require('./Store');

var _dashboards = [{
		'name' : 'Management Dashboard',
		'slug' : 'management-dashboard',
	}, {
		'name'   : 'NGA Campaign Monitoring',
		'slug'   : 'nga-campaign-monitoring',
		'region' : 'Nigeria'
	}, {
		'name' : 'District Dashboard',
		'slug' : 'district'
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
