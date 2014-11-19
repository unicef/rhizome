'use strict';

var _ = require('lodash');
var lineChart = require('../../component/line-chart');

module.exports = {
	template: require('./template.html'),
	data: function () {
		return {
			missed: [
				[[0, 0], [1, 4], [2, 2]],
				[[0, 1], [1, 1], [2, 3]]
			],
		};
	},
	components: {
		'vue-line-chart': lineChart
	}
};
