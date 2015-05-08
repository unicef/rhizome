'use strict';

var _  = require('lodash');
var d3 = require('d3');

var palette = require('util/colorbrewer');

function _fill(d) {
	// jshint validthis: true
	return _.isNull(d) ? 'transparent' : this.scale(d);
}

function _id(d, i) {
	return d.id || i;
}

function _x(d, i) {
	// jshint validthis: true
	var size = _.isFunction(this.cellSize) ? this.cellSize(d, i) : this.cellSize;
	var pad  = _.isFunction(this.cellPadding) ? this.cellPadding(d, i) : this.cellPadding;

	return (size + pad) * i;
}

function _y(d, i) {
	// jshint validthis: true
	var size = _.isFunction(this.cellSize) ? this.cellSize(d, i) : this.cellSize;
	var pad  = _.isFunction(this.cellPadding) ? this.cellPadding(d, i) : this.cellPadding;

	return (size + pad) * i;
}

function _sortRows(a, b) {
	// jshint validthis: true
	var sortIdx = this.sortCol;

	if (_.isNull(sortIdx)) {
		return -1;
	}

	var left = this.values(a)[sortIdx].value;
	var right = this.values(b)[sortIdx].value;

	if (_.isNull(left)) {
		left = Infinity;
	}

	if (_.isNull(right)) {
		right = Infinity;
	}

	if (left < right) {
		return -1;
	}

	if (left > right) {
		return 1;
	}

	return 0;
}

function _translate(d, i) {
	// jshint validthis: true
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
			marginTop    : 120,
			scale        : d3.scale.quantile().domain([0, 1]).range(palette.YlOrRd[9]),
			series       : [],
			sortable     : true,
			sortCol      : null,
			values       : function (d) { return d.values; },
			x            : _x.bind(this),
			y            : _y.bind(this)
		};
	},

	methods : {
		draw : function () {
			var self    = this;
			var sortIdx = this.sortCol;

			var comparator = _sortRows.bind(this);

			var svg = d3.select(this.$$.canvas);

			var row       = svg.select('.data').selectAll('.row').data(this.series, _id);
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

			// Create rows
			row.on('mouseover', this.onRowHover)
				.sort(comparator)
				.transition().duration(750)
				.attr('transform', transform);

			// Add cells to each row
			var cell = row.selectAll('.cell').data(this.values);

			cell.transition()
				.duration(500)
				.attr({
					'fill'   : this.fill,
					'height' : this.cellSize,
					'width'  : this.cellSize,
					'x'      : this.x
				});

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
				.transition().duration(500)
				.style('opacity', 1);

			cell.exit()
				.transition().duration(300)
				.style('opacity', 0)
				.remove();

			cell.on('mouseover', function (d, i) {
					self.onMouseover(this, d, i);
				})
				.on('mouseout', function () {
					self.onMouseout(this);
				});

			// Y-axis ticks
			var tick = svg.select('.x.axis')
				.selectAll('.tick').data(this.series, _id);

			tick.enter()
				.append('g')
				.attr({
					'class'     : 'tick',
					'transform' : transform,
				})
				.style('opacity', 0)
				.transition()
				.duration(300)
				.style('opacity', 1);

			tick.exit()
				.transition()
				.duration(300)
				.style('opacity', 0)
				.remove();

			tick.sort(comparator)
				.transition().duration(750)
				.attr('transform', transform)
				.style('opacity', 1);

			// Y-axis labels
			var label = tick.selectAll('text').data(function (d) { return [d.name]; });

			label.enter()
				.append('text')
				.attr({
					'text-anchor' : 'end',
					'dy' : '1em'
				});

			label.text(String);

			// Dynamically set the left margin to fit all the labels
			this.marginLeft = 4 + _(label)
				.flatten()
				.map(function (el) { return el.getBoundingClientRect(); })
				.pluck('width')
				.max();

			// X-axis column ticks
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
				.style('opacity', 0)
				.transition()
				.duration(300)
				.style('opacity', 1);

			tick
				.on('click', this.setSort)
				.style('font-weight', function (d, i) {
					return i === sortIdx ? 'bold' : 'normal';
				});

			tick.exit()
				.transition().duration(300)
				.style('opacity', 0)
				.remove();

			label = tick.selectAll('text').data(function (d) { return [d]; }, _id);

			label.enter().append('text')
				.attr({
					'transform' : 'translate(4,0) rotate(-45)',
				});

			label.text(String);
		},

		onRowHover : function (d, row) {
			d3.select(this.$$.canvas).selectAll('.row')
				.transition().duration(300)
				.style('opacity', function (d, i) {
					return i === row ? 1 : 0.4;
				});
		},

		onRowOut : function () {
			d3.select(this.$$.canvas).selectAll('.row')
				.transition().duration(300)
				.style('opacity', 1);
		},

		onMouseover : function (el, d, i) {
			var p = d3.select(el.parentNode).datum();

			this.$dispatch('tooltip-show', {
				el   : el,
				data : {
					indicator : this.columnLabels[i],
					region    : p.name,
					template  : 'tooltip-heatmap',
					value     : d.value,
				}
			});
		},

		onMouseout : function (el) {
			this.$dispatch('tooltip-hide', { el : el });
		},

		setSort : function (d, i) {
			this.sortCol = (i === this.sortCol) ? null : i;
		}
	},

	watch : {
		'sortCol'  : 'draw',
		'series'   : 'draw',
		'width'    : 'draw',
		'height'   : 'draw',
		'sortable' : 'draw'
	}
};
