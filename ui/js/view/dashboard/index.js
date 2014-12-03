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
		'chart-axis'          : require('../../component/chart/axis'),
		'chart-base'          : require('../../component/chart'),
		'chart-line'          : require('../../component/chart/line'),
		'chart-pie'           : require('../../component/chart/pie'),
		'chart-arc'           : require('../../component/chart/arc'),
		'chart-stacked'       : require('../../component/chart/stacked'),
		'chart-bullet'        : require('../../component/chart/bullet')
	},

	partials: {
		'y-grid' : require('../../component/chart/yAxis.html'),
		'y-ticks': require('../../component/chart/yAxis.html'),
		'x-ticks': require('../../component/chart/xAxis.html')
	}
};
