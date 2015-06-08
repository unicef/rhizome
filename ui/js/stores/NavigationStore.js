'use strict';

var Reflux = require('reflux/src');

var NavigationStore = Reflux.createStore({
	data : {
		dashboards : [{
			'name' : 'Management: Country',
			'url'  : '/datapoints/management-dashboard',
		}, {
			'name' : 'Management: Districts',
			'url'  : '/datapoints/district'
		}, {
			'name'    : 'NGA Campaign Monitoring',
			'url'     : '/datapoints/nga-campaign-monitoring',
			'region'  : 'Nigeria',
			'offices' : [1]
		}]
	}
});

module.exports = NavigationStore;
