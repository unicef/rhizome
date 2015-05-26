'use strict';

var _    = require('lodash');
var d3   = require('d3');

var label = require('component/chart/renderer/label');

var defaults = {
	margin    : {
		top    : 12,
		right  : 0,
		bottom : 12,
		left   : 0
	},
	name      : _.partial(_.get, _, 'name', ''),
	padding   : 0.1,
	values    : _.identity,
	x         : _.property('x'),
	xFormat   : String,
	y         : _.property('y'),
	y0        : _.partial(_.get, _, 'y0', 0),
	yFormat   : String,
	yScale    : d3.scale.linear
};

function ColumnChart() {}

_.extend(ColumnChart.prototype, {
	defaults : defaults,

	update : function (data, options) {
		var options = _.assign(this._options, options);
		var margin  = options.margin;

		var h = this._height - margin.top - margin.bottom;
		var w = this._width - margin.left - margin.right;

		var domain;

		if (_.isFunction(options.domain)) {
			domain = options.domain(data);
		} else {
			domain = _(data).map(options.values).flatten().map(options.x).value();
		}

		var xScale = d3.scale.ordinal()
			.domain(domain)
			.rangeBands([0, w], options.padding);

		var x = _.flow(options.x, xScale)

		var range;
		if (_.isFunction(options.range)) {
			range = options.range(data);
		} else {
			range = d3.extent(_(data).map(options.values).flatten().value(), function (d) {
				return options.y0(d) + options.y(d);
			});
			// Make sure we always have at least a 0 baseline
			range[0] = Math.min(0, range[0]);
		}
		var yScale = options.yScale()
			.domain(range)
			.range([h, 0]);

		var y = function (d) { return yScale(options.y0(d) + options.y(d)); };

		var height = function (d) {
			var y0 = options.y0(d);
			var y  = options.y(d);

			return yScale(y0) - yScale(y0 + y);
		};

		var svg    = this._svg;
		var g      = svg.select('.data');
		var series = g.selectAll('.bar').data(data);

		series.enter().append('g')
			.attr('class', 'bar');

		series
			.transition()
			.duration(500)
			.style('fill', options.color);

		series.exit()
			.transition()
			.duration(500)
			.style('opacity', 0)
			.remove();

		var column = series.selectAll('rect').data(options.values);

		column.enter()
			.append('rect')
			.style('fill', 'inherit');

		column.attr({
			'height' : height,
			'width'  : xScale.rangeBand(),
			'x'      : x,
			'y'      : y,
		});

		column.exit().remove();

		svg.select('.x.axis')
			.call(d3.svg.axis()
				.orient('bottom')
				.tickSize(0)
				.tickPadding(4)
				.tickValues(_.filter(xScale.domain(), function (d, i, domain) {
					// Include every fourth tick value unless that tick is within three
					// ticks of the last value. Always include the last tick. We have to
					// do this manually because D3 ignores the ticks() value for
					// ordinal scales
					return (i % 4 === 0 && i + 3 < domain.length) || (i + 1) === domain.length;
				}))
				.tickFormat(options.xFormat)
				.scale(xScale));

		var svgBox = this._svg.node().getBoundingClientRect();
		svg.selectAll('.x.axis text')
			.attr('dx', function () {
				var bbox = this.getBoundingClientRect();
				var dx   = null;

				if (bbox.right > svgBox.right) {
					dx = svgBox.right - bbox.right;
				}

				if (bbox.left < svgBox.left) {
					dx = svgBox.left - bbox.left;
				}

				return dx;
			});

		svg.select('.y.axis')
			.call(d3.svg.axis()
				.orient('right')
				.tickFormat(options.yFormat)
				.tickSize(w)
				.ticks(3)
				.scale(yScale));

		svg.selectAll('.y.axis text')
			.attr({
				'dx' : -w,
				'dy' : -4
			});

		var fmt = _.flow(options.y, options.yFormat);
		var labels = _(data)
			.map(function (s) {
				return _.assign({},
					_.max(options.values(s), options.x),
					{ name : options.name(s) }
				);
			})
			.map(function (d) {
				return {
					text    : d.name + ' ' + fmt(d),
					x       : x(d),
					y       : y(d),
					defined : _.isFinite(d.value)
				};
			})
			.reverse()
			.value();

		svg.select('.annotation').selectAll('.series.label')
			.data(labels)
			.call(label()
				.addClass('series')
				.width(w)
				.height(h)
				.align(false));
	}

});

module.exports = ColumnChart;
