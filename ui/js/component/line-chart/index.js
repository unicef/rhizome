/* global window */
'use strict';

var _ = require('lodash');
var d3 = require('d3');
var dom = require('../../util/dom');

function sum(values) {
	return _.reduce(values, function (total, v) {
		return total + v;
	}, 0);
}

function chain(matrix) {
	return _.reduce(matrix, function (combined, v) {
		return combined.concat(v);
	}, []);
}

module.exports = {
	data: function () {
		return {
			height: 1,
			margin: { top: 14, right: 7, bottom: 14, left: 7 },
			series: [],
			width: 1
		};
	},

	created: function () {
		var self = this;

		this._x    = d3.scale.linear();
		this._y    = d3.scale.linear();
		this._line = d3.svg.line()
			.x(function (d) { return self._x(d[0]); })
			.y(function (d) { return self._y(d[1]); });
	},

	ready: function () {
		this._svg   = d3.select(this.$el).append('svg').attr('class', 'line');
		this._chart = this._svg.append('g');

		this._chart.append('rect').attr('class', 'bg');
		this._chart.append('g').attr('class', 'x axis');
		this._chart.append('g').attr('class', 'y axis');
		this._chart.append('g').attr('class', 'series');

		// Trigger initial size calculation.
		this.handleEvent();

		// Update the element's size when the parent resizes.
		window.addEventListener('resize', this);

		this.$watch('series', this._invalidateSize);
	},

	computed: {
		contentHeight: function () {
			return Math.max(1, this.height - sum(_.pick(this.margin, 'top', 'bottom')));
		},

		contentWidth: function () {
			return Math.max(1, this.width - sum(_.pick(this.margin, 'left', 'right')));
		},

	},

	methods: {
		handleEvent: function () {
			var content = dom.contentArea(this.$el.parentElement);

			this.width  = content.width;
			this.height = content.height;

			this._invalidateSize();
		},

		_invalidateSize: function () {
			var points = chain(this.series);

			this._x.domain(d3.extent(points, function (d) { return d[0]; }));
			this._y.domain(d3.extent(points, function (d) { return d[1]; }));

			this._x.range([0, Math.max(1, this.contentWidth)]);
			this._y.range([Math.max(1, this.contentHeight), 0]);

			this._draw();
		},

		_draw: function () {
			this._svg.attr('width', this.width)
					.attr('height', this.height)
				.select('.bg')
					.attr('width', this.contentWidth)
					.attr('height', this.contentHeight);

			this._chart.attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')');

			var series = this._chart.select('.series').selectAll('path')
				.data(this.series);

			series.transition()
				.duration(300)
				.attr('d', this._line);

			series.enter()
				.append('path')
				.attr('d', this._line);

			series.exit().remove();

			this._chart.select('.x')
					.attr('transform', 'translate(0,' + this.contentHeight + ')')
				.call(d3.svg.axis()
					.scale(this._x)
					.tickSize(0)
					.orient('bottom'));

			this._chart.select('.y')
				.call(d3.svg.axis()
					.scale(this._y)
					.orient('right')
					.tickSize(this.contentWidth))
				.selectAll('text')
					.attr('x', 4)
					.attr('dy', -4);
		}

	}
};
