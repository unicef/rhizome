'use strict';

var _  = require('lodash');
var d3 = require('d3');

var qualitativeAxis = require('./qualitative-axis');

var defaults = {
	domain     : _.constant([0, 1]),
	fontSize   : 12,
	lineHeight : 2,
	padding    : 0.1,
	scale      : d3.scale.linear,
	thresholds : [],
	targets    : [],
	format     : String,

	margin : {
		top    : 12,
		right  : 0,
		bottom : 12,
		left   : 0
	}
};

function BulletChart() {}

_.extend(BulletChart.prototype, {
	defaults : defaults,

	initialize : function (el, data, options) {
		options = this._options = _.defaults({}, options, defaults);

		var n = Math.max(data.length, 1);
		var height = options.fontSize * n * options.lineHeight +
			options.fontSize * options.padding * (n - 1) +
			options.margin.top +
			options.margin.bottom;

		this._width  = el.clientWidth;

		var svg = this._svg = d3.select(el).append('svg')
			.attr({
				'viewBox' : '0 0 ' + this._width + ' ' + height,
				'width'   : this._width,
				'height'  : height
			});

		// Append the x-axis container and a blank background
		svg.append('g').attr('class', 'x axis');

		// Append a data layer
		svg.append('g')
			.attr({
				'class'     : 'data',
				'transform' : 'translate(' + options.margin.left + ',' + options.margin.top + ')'
			});

		this.update(data);
	},

	update : function (data, options) {
		options = _.assign(this._options, options);

		var margin  = options.margin;
		var svg     = this._svg;

		var n = Math.max(data.length, 1);
		var h = options.fontSize * n * options.lineHeight + options.fontSize * options.padding * (n - 1);
		var w = this._width - margin.left - margin.right;

		var yScale = d3.scale.ordinal()
			.domain(_(data).flatten().map(options.y).uniq().value())
			.rangeRoundBands([h, 0]);

		var y = _.flow(options.y, yScale);

		var xScale = options.scale()
			.domain(options.domain(data))
			.range([0, w]);

		var x     = _.flow(options.marker, xScale);
		var width = _.flow(options.value, xScale);

		var isEmpty = !_(data).map(options.value).all(_.isFinite);

		// Draw qualitative ranges
		if (!(isEmpty || _.isEmpty(options.thresholds) || _.isEmpty(options.targets))) {
			svg.select('.x.axis')
				.call(qualitativeAxis()
					.height(h + margin.top + margin.bottom)
					.scale(xScale)
					.threshold(d3.scale.threshold()
						.domain(options.thresholds)
						.range(options.targets)
					)
				);
		} else {
			svg.select('.x.axis')
				.call(qualitativeAxis()
					.height(h + margin.top + margin.bottom)
					.scale(xScale)
					.threshold(d3.scale.threshold()
						.domain([])
						.range([''])
					)
					.colors(['#F2F2F2', '#F2F2F2'])
				);
		}

		svg.attr({
			'viewBox' : '0 0 ' + w + ' ' + (h + margin.top + margin.bottom),
			'width'   : w,
			'height'  : h + margin.top + margin.bottom
		});

		var g = svg.select('.data')
				.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

		// Draw value
		var bar = g.selectAll('.bar').data(data);

		bar.enter().append('g');
		bar
			.attr({
				'class'  : 'bar',
				'y'      : y,
			})
			.style('fill', options.fill);
		bar.exit().remove();

		var value = bar.selectAll('.value').data(function (d) { return isEmpty ? [] : [d]; });

		var valueAttr = {
			'class'  : 'value',
			'height' : yScale.rangeBand()
		};

		value.enter()
			.append('rect')
			.attr(valueAttr)
			.style('fill', 'inherit');

		value.attr(valueAttr).attr('width', width);
		value.exit().remove();

		// Draw comparitive measure
		var measure = bar.selectAll('.comparative-measure')
			.data(function (d) {
				var v = options.value(d);
				var m = options.marker(d);
				return _.isFinite(v) && _.isFinite(m) ? [d] : [];
			});

		var measureHeight = yScale.rangeBand() * 0.4;

		var initAttr = {
			'class'  : 'comparative-measure',
			'width'  : 3,
			'height' : yScale.rangeBand() + measureHeight,
			'y'      : -measureHeight / 2,
		};

		measure.enter().append('rect').attr(initAttr).style('fill', 'inherit');
		measure.attr(initAttr).attr('x', x);
		measure.exit().remove();

		var label = bar.selectAll('text')
			.data(function (d) {
				var v = options.value(d);
				return _.isFinite(v) ? [v] : [];
			});

		label.enter()
			.append('text')
			.attr({
				'class'     : 'label',
				'dx'        : '4'
			});

		label
			.attr({
				'dy'        : (options.lineHeight / 4) + 'em',
				'transform' : 'translate(0,' + (h / 2) + ')'
			})
			.style('font-size', options.fontSize)
			.text(options.format);
		label.exit().remove();
	},

	resize : function (el) {

	}
});

module.exports = BulletChart;
