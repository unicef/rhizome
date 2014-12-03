'use strict';

module.exports = {
	template: require('./template.html'),
	replace: true,

	data: function () {
		return {
			dashboard: 'management-dashboard',
			region: 23, // Nigeria
			date: ''
		};
	},

	components: {
		'management-dashboard': require('../../dashboard/management'),
		'chart-base'          : require('../../component/chart'),
		'chart-pie'           : require('../../component/chart/pie'),
		'chart-stackedTime'   : require('../../component/chart/stackedTime')
	}
};
