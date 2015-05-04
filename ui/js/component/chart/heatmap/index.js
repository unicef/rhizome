'use strict';

var palette = require('util/colorbrewer');
var util    = require('util/data');

module.exports = {
	template : require('./template.html'),

	data : function () {
		return {
			columnLabels : [],
			series       : []
		};
	},

	methods : {
		onMouseover : function (v, i, vm) {
			this.$dispatch('tooltip-show', {
				el : vm.$el,
				data : {
					indicator : this.columnLabels[i],
					region    : vm.$parent.name,
					template  : 'tooltip-heatmap',
					value     : v,
				}
			});
		},

		onMouseout : function (vm) {
			this.$dispatch('tooltip-hide', { el : vm.$el });
		}
	},

	filters : {
		color : function (value) {
			var scale = d3.scale.ordinal()
				.domain(['bad', 'okay', 'ok', 'good'])
				.range(['#AF373E', 'rgb(112,118,119)', 'rgb(112,118,119)','#2B8CBE'])

			return !!value ? scale(value) : 'transparent';
		}
	}
};
