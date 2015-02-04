'use strict';

module.exports = {
	template: require('./nco.html'),

	data: function () {
		return {
			region  : null,
			campaign: null,

			overview: [{
				title     : 'Influencer',
				indicators: [164,165,166,167],
				chart     : 'chart-bar'
			}, {
				title     : 'Information Source',
				indicators: [164,165,166,167],
				chart     : 'chart-bar'
			}, {
				title     : 'Reasons for Missed',
				indicators: [164,165,166,167],
				chart     : 'chart-bar'
			}, {
				title     : 'Reasons for Absence',
				indicators: [164,165,166,167],
				chart     : 'chart-bar'
			}, {
				title     : 'Reasons for NC',
				indicators: [164,165,166,167],
				chart     : 'chart-bar'
			}, {
				title     : 'NC Resolved by',
				indicators: [164,165,166,167],
				chart     : 'chart-bar'
			}]
		};
	},

	components: {

	}
};
