'use strict';

var _  = require('lodash');
var d3 = require('d3');

var palette = require('util/colorbrewer');
var util    = require('util/data');

function _fill(d) {
	return _.isNull(d) ? 'transparent' : this.scale(d.value);
}

function _id(d, i) {
	return d.id || i;
}

function _x(d, i) {
	var size = _.isFunction(this.cellSize) ? this.cellSize(d, i) : this.cellSize;
	var pad  = _.isFunction(this.cellPadding) ? this.cellPadding(d, i) : this.cellPadding;

	return (size + pad) * i;
}

function _y(d, i) {
	var size = _.isFunction(this.cellSize) ? this.cellSize(d, i) : this.cellSize;
	var pad  = _.isFunction(this.cellPadding) ? this.cellPadding(d, i) : this.cellPadding;

	return (size + pad) * i;
}

function _translate(d, i) {
	return 'translate(0,' + this.y(d, i) + ')';
}

module.exports = {
	template : require('./template.html'),

	mixins : [
		require('../mixin/resize'),
		require('../mixin/margin')
	],

	data : function () {
		return {
			cellPadding  : 2,
			cellSize     : 14,
			columnLabels : [],
			fill         : _fill.bind(this),
			scale        : d3.scale.quantile().domain([0, 1]).range(palette.YlOrRd[9]),
			series       : [],
			values       : function (d) { return d.values; },
			x            : _x.bind(this),
			y            : _y.bind(this)
		};
	},

	methods : {
		draw : function () {
			var svg = d3.select(this.$$.canvas);

			var row = svg.select('.data').selectAll('.row').data(this.series, _id);
			var transform = _translate.bind(this);

			row.enter().append('g')
				.attr({
					'class'     : 'row',
					'transform' : transform,
				});

			row.exit()
				.transition().duration(300)
				.style('opacity', 0)
				.remove();

			var cell = row.selectAll('.cell').data(this.values);

			cell.enter().append('rect')
				.attr({
					'class'  : 'cell',
					'height' : this.cellSize,
					'x'      : this.x,
					'width'  : this.cellSize,
				})
				.style({
					'opacity' : 0,
					'fill'    : this.fill
				})

			cell.exit()
				.transition().duration(300)
				.style('opacity', 0)
				.remove();

			var t = svg.transition().duration(500);

			t.selectAll('.row')
					.attr('transform', transform)
				.selectAll('.cell')
					.attr({
						'x'      : this.x,
						'width'  : this.cellSize,
						'height' : this.cellSize
					})
					.style({
						'opacity' : 1,
						'fill'    : this.fill
					});

			var tick = svg.select('.x.axis')
				.selectAll('.tick').data(this.series, _id);

			tick.enter()
				.append('g')
				.attr({
					'class'     : 'tick',
					'transform' : transform,
				})
				.style('opacity', 0);

			tick.exit()
				.transition()
				.duration(300)
				.style('opacity', 0)
				.remove();

			var label = tick.selectAll('text').data(function (d) { return [d.name]; });

			label.enter()
				.append('text')
				.attr({
					'text-anchor' : 'end',
					'dy' : '1em'
				});

			label.text(String);

			t.select('.x.axis').selectAll('.tick')
				.attr('transform', transform)
				.style('opacity', 1);

			this.marginLeft = 4 + _(label)
				.flatten()
				.map(function (el) { return el.getBoundingClientRect(); })
				.pluck('width')
				.max();

			tick = svg.select('.y.axis').selectAll('.tick').data(this.columnLabels, _.identity);

			var x = this.x;

			tick.enter()
				.append('g')
				.attr({
					'class' : 'tick',
					'transform' : function (d, i) {
						return 'translate(' + x(d, i) + ',0)';
					}
				})
				.style('opacity', 0);

			tick.exit()
				.transition().duration(300)
				.style('opacity', 0)
				.remove();

			var label = tick.selectAll('text').data(function (d) { return [d]; }, _id);

			label.enter().append('text')
				.attr({
					'transform' : 'translate(4,0) rotate(-45)',
				});

			label.text(String);

			t.select('.y.axis').selectAll('.tick')
				.style('opacity', 1);
		},

		onRowHover : function (row) {
			d3.select(this.$el).selectAll('tbody tr')
				.transition().duration(300)
				.style('opacity', function (d, i) {
					return i === row ? 1 : 0.4;
				});
		},

		onRowOut : function () {
			d3.select(this.$el).selectAll('tbody tr')
				.transition().duration(300)
				.style('opacity', 1);
		},

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
	},

	watch : {
		'series' : 'draw',
		'width'  : 'draw',
		'height' : 'draw'
	}
};
