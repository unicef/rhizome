'use strict';

module.exports = {
	template: require('./nco.html'),

	data: function () {
		return {
			region  : null,
			campaign: null,

			overview: [{
				title     : 'Influencer',
				indicators: [287,288,289,290,291,292,293,294],
				chart     : 'chart-bar'
			}, {
				title     : 'Information Source',
				indicators: [307,308,309,310,311,312,313,314,315,316,317],
				chart     : 'chart-bar'
			}, {
				title     : 'Reasons for Missed',
				indicators: [318,319,320,321,322],
				chart     : 'chart-bar'
			}, {
				title     : 'Reasons for Absence',
				indicators: [323,324,325,326,327],
				chart     : 'chart-bar'
			}, {
				title     : 'Reasons for NC',
				indicators: [328,329,330,331,332,333,334],
				chart     : 'chart-bar'
			}, {
				title     : 'NC Resolved by',
				indicators: [345,346,347,348],
				chart     : 'chart-bar'
			}]
		};
	},

	components: {

	}
};
