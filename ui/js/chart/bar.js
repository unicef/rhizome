'use strict';

var _  = require('lodash');
var d3 = require('d3');

var ColumnChart = require('./column');

var browser = require('util/browser');
var color   = require('util/color');
var legend  = require('component/chart/renderer/legend');

var defaults = {
	barHeight : 14,
	name      : _.partial(_.get, _, 'name', ''),
	padding   : 0.1,
	values    : _.property('values'),
	x         : _.property('x'),
	x0        : _.partial(_.get, _, 'x0', 0),
	xFormat   : String,
	xScale    : d3.scale.linear,
	y         : _.property('y'),
	yFormat   : String,

	margin : {
		top    : 9,
		right  : 18,
		bottom : 18,
		left   : 80
	}
};

function BarChart () {}

_.extend(BarChart.prototype, ColumnChart.prototype, {
	defaults : defaults,

	update : function (data, options) {
		var options = _.assign(this._options, options);
		var margin  = options.margin;

		var l = _(data).map(options.values).map('length').max();
		var h = l * options.barHeight + (l - 1) * options.barHeight * options.padding;
		var w = this._width - margin.left - margin.right;

		var range;
		if (_.isFunction(options.range)) {
			range = options.range(data);
		} else {
			range = d3.extent(_(data).map(options.values).flatten().value(), function (d) {
				return options.x0(d) + options.x(d);
			});

			// Make sure we always have at least a 0 baseline
			range[0] = Math.min(0, range[0]);
		}

		var xScale = options.xScale()
			.domain(range)
			.range([0, w]);

		var x = _.flow(options.x0, xScale);

		var width = function (d) {
			var x0 = options.x0(d);
			var x  = options.x(d);

			return xScale(x0 + x) - xScale(x0);
		};

		var domain;
		if (_.isFunction(options.domain)) {
			domain = options.domain(data);
		} else {
			domain = _(data).map(options.values).flatten().map(options.y).value();
		}

		var yScale = d3.scale.ordinal()
			.domain(domain)
			.rangeBands([h, 0], options.padding);

		var y = _.flow(options.y, yScale);

		var colorScale = _.flow(
			options.name,
			color.scale(_.map(data, options.name))
		);

		var svg    = this._svg;
		var g      = svg.select('.data');
		var series = g.selectAll('.bar').data(data);

		var canvasH = h + margin.top + margin.bottom;
		var canvasW = w + margin.left + margin.right;

		svg.attr('viewBox', '0 0 ' + canvasW + ' ' + canvasH);

		if (browser.isIE()) {
			svg.attr({
				'width'  : canvasW,
				'height' : canvasH
			});
		}

		svg.select('.bg')
			.attr({
				'height': h,
				'width' : w,
				'x'     : margin.left,
				'y'     : margin.top
			});

		series.enter().append('g')
			.attr('class', 'bar');

		series.style('fill', colorScale);

		series.exit()
			.transition()
			.duration(500)
			.style('opacity', 0)
			.remove();

		var hover = d3.dispatch('over', 'out');

		var bar = series.selectAll('rect').data(options.values);

		bar.enter()
			.append('rect')
			.style('fill', 'inherit');

		bar.attr({
				'height' : yScale.rangeBand(),
				'width'  : width,
				'x'      : x,
				'y'      : y,
			})
			.on('mouseover', hover.over)
			.on('mouseout', hover.out);

		bar.exit().remove();

		svg.select('.x.axis')
			.call(d3.svg.axis()
				.orient('bottom')
				.tickSize(h)
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

		svg.select('.y.axis')
			.call(d3.svg.axis()
				.orient('left')
				.tickFormat(options.yFormat)
				.ticks(3)
				.scale(yScale));

		hover.on('out', function (d, i) {
			options.onMouseOut(d, i, this);
		});

		hover.on('over', function (d, i) {
			options.onMouseOver(d, i, this);
		});
	}
});

module.exports = BarChart;
