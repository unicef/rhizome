'use strict';

var _     = require('lodash');
var d3    = require('d3');

var color = require('util/color');

module.exports = {

	replace : true,
	template: require('./bar.html'),

	mixins: [
		require('./mixin/margin'),
		require('./mixin/resize')
	],

	paramAttributes: [
		'data-format'
	],

	data: function () {
		return {
			aspect       : false, // Disable auto-setting height
			barHeight    : 14,
			format       : 's',
			marginTop    : 9,
			marginBottom : 9,
			marginLeft   : 80,
			padding      : 1,
			series       : []
		};
	},

	computed: {
		categories: function () {
			return _(this.series)
				.pluck('values')
				.flatten()
				.pluck('y')
				.uniq()
				.value();
		},

		empty: function () {
			return !this.series || this.series.length < 1;
		},

		height: function () {
			var l       = this.categories.length;
			var padding = l * this.padding;
			var h       = Math.max(0, l * this.barHeight + padding);

			return h + this.marginTop + this.marginBottom;
		}
	},

	methods: {

		draw: function () {
			if (this.empty) {
				return;
			}

			var svg = d3.select(this.$el);

			var data = _(this.series)
				.pluck('values')
				.flatten();

			var xScale = d3.scale.linear()
				.range([0, this.contentWidth]);

			if (this.domain) {
				xScale.domain(this.domain);
			} else {
				xScale.domain([0, d3.max(data.value(), function (d) {
					return d.x;
				})]);
			}

			var x = function (d) {
				return xScale(d.x);
			};

			var yScale = d3.scale.ordinal()
				.domain(this.categories)
				.rangePoints([this.contentHeight, 0]);

			var y = function (d) {
				return yScale(d.y);
			};

			var series = svg.select('.data')
				.selectAll('.series')
				.data(this.series, function (d) {
					return d.name;
				});

			series.enter().append('g').attr('class', 'series');

			var height = this.barHeight;

			series.attr('transform', function (d, i) {
				return 'translate(0,' + ((i * height) - height / 2) + ')';
			});

			var colorScale = color.scale(_.pluck(this.series, 'name'));
			var fmt        = d3.format(this.format);

			series.each(function (datum) {
				var g   = d3.select(this);

				var bar = g.selectAll('.bar')
					.data(datum.values);

				bar.transition()
					.duration(300)
					.attr('transform', function (d) {
						return 'translate(0,' + y(d) + ')';
					});

				var barEnter = bar.enter()
					.append('g')
					.attr('class', 'bar');

				barEnter.append('rect')
					.attr('width', 0);

				barEnter.append('text')
					.attr({
						'x'  : '0.1em',
						'y'  : height / 2,
						'dy' : '0.35em'
					});

				bar.select('rect')
					.transition()
					.duration(300)
					.attr({
						'fill'   : colorScale(datum.name),
						'height' : height,
						'width'  : x,
					});

				bar.select('text')
					.text(function (d) {
						return fmt(d.x);
					})
					.transition()
					.duration(300)
					.attr('y', height / 2);

				bar.exit()
					.select('rect')
					.transition()
					.duration(300)
					.attr('width', 0);

				d3.timer(function () {
					bar.exit().remove();
				}, 0, 300);
			});

			series.exit()
				.transition()
				.duration(300)
				.style('opacity', 0)
				.remove();

			var yAxis = d3.svg.axis()
				.orient('left')
				.tickSize(0)
				.scale(yScale);

			svg.select('.y.axis')
				.call(yAxis);
		}

	},

	watch: {
		'series' : 'draw',
		'width'  : 'draw',
		'height' : 'draw'
	}

};
