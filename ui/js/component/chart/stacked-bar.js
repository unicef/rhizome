'use strict';

var _     = require('lodash');
var d3    = require('d3');

var color = require('util/color');

module.exports = {

	mixins : [
		require('./bar')
	],

	data : function () {
		return {
			'offset' : 'zero'
		};
	},

	computed : {

		height : function () {
			var l       = this.categories.length;
			var padding = l * this.padding;
			var h       = Math.max(0, l * this.barHeight + padding);

			return h + Number(this.marginTop) + Number(this.marginBottom);
		}

	},

	methods : {

		draw : function () {
			var self = this;
			var svg  = d3.select(this.$el);

			// d3.layout.stack stacks the y-value, but we want to stack the x value,
			// so we swap x and y in the layout definition.
			var stack = d3.layout.stack()
				.values(function (d) {
					return d.values;
				})
				.offset(this.offset)
				.order('default')
				.x(function (d) {
					return d.y;
				})
				.y(function (d) {
					return d.x;
				})
				.out(function (d, y0, y) {
					d.x0 = y0;
					d.x  = y;
				});

			// We have to make a deep clone of the data because d3.layout.stack
			// modifies the data, which prevents us from toggling different
			// offset modes
			var data = stack(_.cloneDeep(this.series));

			var xScale = d3.scale.linear()
				.range([0, this.contentWidth])
				.domain([0, d3.max(_(data).pluck('values').flatten().value(), function (d) {
					return d.x0 + d.x;
				})]);

			var x = function (d) {
				return xScale(d.x0);
			};

			var width = function (d) {
				return xScale(d.x);
			};

			var yScale = d3.scale.ordinal()
				.domain(this.categories)
				.rangePoints([this.contentHeight, 0], this.padding);

			var y = function (d) {
				return yScale(d.y);
			};

			var series = svg.select('.data')
				.selectAll('.series')
				.data(data, function (d) {
					return d.name;
				});

			var height = this.barHeight;

			series.enter().append('g').attr({
				'class'     : 'series',
				'transform' : 'translate(0,' + (-height / 2) + ')'
			});

			var colorScale = color.scale(_.pluck(data, 'name'));
			var fmtString  = (this.offset === 'expand') ? '%' : this.format;
			var fmt        = d3.format(fmtString);

			series.each(function (datum) {
				var g = d3.select(this);

				var bar = g.selectAll('.bar')
					.data(datum.values);

				bar.enter()
					.append('rect')
					.attr({
						'class'  : 'bar',
						'x'      : x,
						'y'      : y,
						'height' : height,
						'width'  : 0,
						'fill'   : colorScale(datum.name)
					})
					.on('mousemove', function (d) {
						var evt = d3.event;

						// Shadow the formatter because otherwise the closure keeps a
						// reference to the formatter that was used when the rect was
						// created and doesn't pick up on changes to the offset property.
						var fmt = d3.format((self.offset === 'expand') ? '%' : self.format);

						self.$dispatch('tooltip-show', {
							el       : this,
							position : {
								x : evt.pageX,
								y : evt.pageY
							},
							data : {
								template : 'tooltip-stacked-bar',
								series   : d3.select(this.parentNode).datum().name,
								y        : d.y,
								x        : fmt(d.x)
							}
						});
					})
					.on('mouseout', function () {
						self.$dispatch('tooltip-hide', { el: this });
					});

				bar.transition()
					.duration(300)
					.attr({
						'x'      : x,
						'y'      : y,
						'height' : height,
						'width'  : width
					});

				bar.exit()
					.transition()
					.duration(300)
					.attr('width', 0)
					.remove();
			});

			var xAxis = d3.svg.axis()
				.orient('bottom')
				.tickSize(-this.contentHeight)
				.ticks(Number(this.tickCount))
				.tickFormat(fmt)
				.tickPadding(height / 2)
				.scale(xScale);

			svg.select('.x.axis')
				.call(xAxis);

			var yAxis = d3.svg.axis()
				.scale(yScale)
				.tickSize(0)
				.orient('left');

			svg.select('.y.axis')
				.call(yAxis);
		}

	},

	watch : {
		'offset' : 'draw'
	}

};
