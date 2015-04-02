'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var RADIUS       = 3;
var HOVER_RADIUS = 5;

function x(d) {
	return d.x;
}

function y(d) {
	return d.y;
}

module.exports = {

	template: require('./chart.html'),
	replace : true,

	paramAttributes: [
		'data-format-x',
		'data-format-y',
		'data-x-axis-label',
		'data-y-axis-label'
	],

	mixins: [
		require('component/chart/mixin/margin'),
		require('component/chart/mixin/resize')
	],

	data: function () {
		return {
			marginLeft   : 24,
			marginBottom : 24,
			series       : [],
			formatX      : 's',
			formatY      : 's',
			chartType    : 'scatter',
			domain       : null,
			range        : null,
			xAxisLabel   : '',
			yAxisLabel   : ''
		};
	},

	computed: {
	},

	methods: {
		draw : function () {
			function cx(d) {
				return xScale(d.x);
			}

			function cy(d) {
				return yScale(d.y);
			}

			var self = this;
			var svg  = d3.select(this.$el);

			var series = this.series || [];

			var xScale = d3.scale.linear()
				.range([0, this.contentWidth]);

			if (!this.domain) {
				xScale.domain([0, d3.max(series, function (d) { return d.x; })]);
			} else {
				xScale.domain(this.domain);
			}

			var yScale = d3.scale.linear()
				.range([this.contentHeight, 0]);

			if (!this.range) {
				yScale.domain([0, d3.max(series, function (d) { return d.y; })]);
			} else {
				yScale.domain(this.range);
			}

			var point = svg
				.select('.data')
				.selectAll('.point')
				.data(series, function (d, i) {
					return d.id || i;
				});

			// FIXME: Hard-coded transition speed
			point
				.transition()
				.duration(500)
				.attr({
					'cx': cx,
					'cy': cy
				});

			// FIXME: Hard-coded transition speed
			point.enter()
				.append('circle')
				.attr({
					'class': 'point',
					'cx'   : cx,
					'cy'   : cy,
					'r'    : 0
				})
				.style('fill', '#414849')
				.on('mouseover', function (d) {
					var evt = d3.event;

					d3.select(this)
						.transition()
						.duration(500)
						.ease('elastic')
						.attr('r', HOVER_RADIUS);

					self.$dispatch('tooltip-show', {
						el       : this,
						position : {
							x : evt.pageX,
							y : evt.pageY
						},
						data : {
							// Have to make sure we use the default tooltip, otherwise if a
							// different template was used, this shows the old template
							template : 'tooltip-default',
							text     : d.name,
							delay    : 0
						}
					})
				})
				.on('mouseout', function (d) {
					d3.select(this)
						.transition()
						.duration(500)
						.ease('elastic')
						.attr('r', RADIUS);

					self.$dispatch('tooltip-hide', { el : this });
				})
				.transition()
				.duration(500)
				.attr('r', RADIUS);

			// FIXME: Hard-coded transition speed
			point.exit()
				.transition()
				.duration(500)
				.attr('r', 0)
				.remove();

			var xAxis = d3.svg.axis()
				.scale(xScale)
				.tickFormat(d3.format(this.formatX))
				.ticks(3)
				.tickSize(0)
				.tickPadding(5)
				.orient('bottom');

			svg
				.select('.x.axis')
				.call(xAxis);

			var yAxis = d3.svg.axis()
				.scale(yScale)
				.tickFormat(d3.format(this.formatY))
				.ticks(4)
				.tickSize(-this.contentWidth)
				.orient('left');

			svg
				.select('.y.axis')
				.call(yAxis);
		}
	},

	watch: {
		'series' : 'draw',
		'width'  : 'draw',
		'height' : 'draw'
	}
};
