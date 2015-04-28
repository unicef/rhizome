/* global window */
'use strict';

var _   = require('lodash');

var api = require('data/api');

module.exports = {
	template : require('./district.html'),

	data : function () {
		return {
			annotation     : null,
			campaign       : null,
			currentSection : null,
			highlights     : [],
			region         : null,
			sections       : []
		};
	},

	methods : {
		dataReceived : function (data) {

		},

		error : function () {
			window.alert('Dammit!');
		},

		load : function () {
			var q = {
				parent_region__in : this.region,
				level             : 'district'
			};

			var start = moment(this.campaign.start_date)
				.subtract('1 year')
				.format('YYYY-MM-DD');

			var end = moment(this.campaign.start_date).format('YYYY-MM-DD');

			api.datapoints(_.assign({
					indicator__in  : [431,432,433],
					campaign_start : start,
					campaign_end   : end
				}, q))
				.then(this.dataReceived, this.error);
		}
	},

	watch : {
		campaign : 'load',
		region   : 'load'
	}
};
