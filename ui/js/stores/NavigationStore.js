'use strict';

var Reflux = require('reflux/src');

var NavigationStore = Reflux.createStore({
	init : function () {
		// FIXME: This should fetch data from the server...
		this.data = {
			dashboards : [{
					'name' : 'Management: Country',
					'url'  : '/datapoints/management-dashboard'
				}, {
					'name' : 'Management: Districts',
					'url'  : '/datapoints/district'
				}, {
					'name'    : 'NGA Campaign Monitoring',
					'url'     : '/datapoints/nga-campaign-monitoring',
					'region'  : 'Nigeria',
					'offices' : [1]
				}]
			};
	},

	getInitialState : function () {
		return this.data;
	}
});

module.exports = NavigationStore;
