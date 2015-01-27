'use strict';

var page = require('page');

module.exports = {
	template: require('./template.html'),
	replace: true,

	data: function () {
		return {
			dashboard: 'management-dashboard'
		};
	},

	created: function () {
		var show = function (ctx) {
			console.debug('dashboard::show', ctx.params.dashboard);
			this.dashboard = ctx.params.dashboard || 'management-dashboard';
		}.bind(this);

		page('/datapoints/:dashboard', show);
		page();
	},

	components: {
		'management-dashboard': require('../../dashboard/management'),
		'nco-dashboard'       : require('../../dashboard/nco'),

		'chart-bar'           : require('../../component/chart/bar'),
		'chart-bullet'        : require('../../component/chart/bullet'),
		'chart-map'           : require('../../component/chart/map'),
		'chart-pie'           : require('../../component/chart/pie'),
		'chart-stacked-area'  : require('../../component/chart/stacked-area'),
		'chart-line'          : require('../../component/chart/line'),
		'chart-year-over-year': require('../../component/chart/year-over-year'),
		'vue-dropdown'        : require('../../component/dropdown')
	},

	partials: {
		'loading-overlay': require('../../component/chart/partials/loading-overlay.html')
	}
};
