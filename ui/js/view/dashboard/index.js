'use strict';

module.exports = {
	template: require('./template.html'),
	replace: true,

	data: function () {
		return {
			dashboard: 'management-dashboard'
		};
	},

	components: {
		'management-dashboard': require('../../dashboard/management'),

		'chart-bullet'        : require('../../component/chart/bullet'),
		'chart-map'           : require('../../component/chart/map'),
		'chart-pie'           : require('../../component/chart/pie'),
		'chart-stacked-area'  : require('../../component/chart/stacked-area'),
		'chart-line'          : require('../../component/chart/line'),
		'chart-year-over-year': require('../../component/chart/year-over-year'),
		'vue-dropdown'        : require('../../component/dropdown')
	}
};
