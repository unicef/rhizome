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
			console.log(v, this.columnLabels[i], vm.$parent.name);
		},

		onMouseout : function (vm) {
			this.$dispatch('tooltip-hide', { el : vm.$el });
		}
	},

	filters : {
		color : function (value) {
			var p = palette.RdYlBu[11];
			var scale = d3.scale.quantile()
				.range(d3.range(p.length))
				.domain([1, 0]);

			return util.defined(value) ? p[scale(value)] : 'transparent';
		}
	}
};
