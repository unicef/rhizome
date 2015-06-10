'use strict';

var _      = require('lodash');
var d3     = require('d3');

var legend = require('./renderer/legend');

module.exports = {

	paramAttributes : [
		'data-click-event'
	],

	mixins : [
		require('./bar')
	],

	data : function () {
		return {
			chartType  : 'stacked-bar',
			clickEvent : 'bar-click',
			offset     : 'zero',
			sortBy     : null,
		};
	},

	computed : {

		height : function () {
			var l       = this.categories().length;
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
				.order(function (data) {
					var order = d3.range(data.length);

					if (self.sortBy) {
						var idx = _.findIndex(self.series, function (d) {
							return d.name === self.sortBy;
						});

						// Move the index of the series on which we're sorting to the front
						if (idx >= 0) {
							order.splice(idx, 1);
							order.unshift(idx);
						}
					}

					return order;
				})
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

			var sortIdx = 0;

			if (self.sortBy) {
				sortIdx = _.findIndex(data, function (d) {
					return d.name === self.sortBy;
				});
			}

			var yScale = d3.scale.ordinal()
				.domain(this.categories(data, sortIdx))
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

			var colorScale = this._color;
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
					})
					.on('click', function (d) {
						self.$dispatch(self.clickEvent, d);
					});

				bar.transition()
					.duration(500)
					.attr({
						'x'      : x,
						'width'  : width
					})
					.transition()
					.duration(500)
					.delay(500)
					.attr({
						'y'      : y,
						'height' : height
					});

				bar.exit()
					.transition()
					.duration(300)
					.attr('width', 0)
					.remove();
			});

			series.exit()
				.transition()
				.duration(300)
				.style('opacity', 0)
				.remove();

			var xAxis = d3.svg.axis()
				.orient('bottom')
				.tickSize(-this.contentHeight)
				.ticks(Number(this.tickCount))
				.tickFormat(fmt)
				.tickPadding(height / 2)
				.scale(xScale);

			var yAxis = d3.svg.axis()
				.scale(yScale)
				.tickSize(0)
				.tickPadding(5)
				.orient('left');

			var t0 = svg.transition().duration(500);
			var t1 = t0.transition().duration(500);


			t0.select('.x.axis')
				.call(xAxis);

			t1.select('.y.axis')
				.call(yAxis);

			if (this.series.length > 1) {
				// Show the legend if we have at least two series
				svg.select('.legend')
					.call(legend()
						.interactive(true)
						.filled(function (d, i) {
							return self.sortBy ? self.sortBy === d : i === 0;
						})
						.scale(colorScale)
						.clickHandler(this.setSortBy));
			} else {
				// Clear the legend if we have fewer than two series
				svg.select('.legend')
					.selectAll('g')
					.remove();
			}
		},

		setSortBy : function (d) {
			this.sortBy = d;
		}

	},

	watch : {
		'offset' : 'draw',
		'sortBy' : 'draw'
	}

};
