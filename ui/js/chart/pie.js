'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var browser = require('util/browser');
var colors  = require('colors');
var legend  = require('chart/renderer/legend');

function _domain(data, options) {
	return [0, _(data).map(options.value).sum()];
}

var DEFAULTS = {
	domain      : _domain,
	innerRadius : 0,
	margin : {
		top    : 0,
		right  : 0,
		bottom : 0,
		left   : 0
	},
	value : _.property('value'),
  name  : _.property('indicator.short_name')
};

function PieChart() {}

_.extend(PieChart.prototype, {
	defaults : DEFAULTS,

	initialize : function (el, data, options) {
		var options = this._options = _.defaults({}, options, DEFAULTS);
		var margin  = options.margin;

		this._height = this._width = _.get(options, 'size', el.clientWidth);

		var svg = this._svg = d3.select(el).append('svg').attr('class', 'pie');

		var g = svg.append('g').attr('class', 'margin');

		g
			.append('g').attr('class', 'data')
			.append('path').attr('class', 'bg');

    g.append('g').attr('class', 'legend');

		this.update(data);
	},

	update : function (data, options) {
		options = _.assign(this._options, options);
		var margin = options.margin;

		data = _(data)
      .filter(d => {
        var v = options.value(d);
        return _.isFinite(v) && v > 0;
      })
      .sortBy(options.value)
      .reverse()
      .value();

		var w = this._width - margin.left - margin.right;
		var h = this._height - margin.top - margin.bottom;
		var s = Math.min(w, h);

		var svg = this._svg;

		svg.attr({
				'viewBox' : '0 0 ' + this._width + ' ' + this._height,
			})
			.style({
				'width'   : this._width + 'px',
				'height'  : this._height + 'px'
			})
			.select('.margin')
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

		var g = svg.select('.data')
			.attr('transform', 'translate(' + (w / 2) + ',' + (h / 2) + ')');

		var arc = d3.svg.arc()
			.innerRadius(s / 2 * options.innerRadius)
			.outerRadius(s / 2);

		svg.select('.bg')
			.datum({
				startAngle : 0,
				endAngle   : 2 * Math.PI
			})
			.attr('d', arc);

		var scale = d3.scale.linear()
			.domain(options.domain(data, options))
			.range([0, 2 * Math.PI]);

		var pie = d3.layout.stack()
			.values (function (d) { return [d]; })
			.x(options.name)
			.y(options.value)
			.out(function (d, y0, y) {
				d.startAngle = scale(y0);
				d.endAngle   = scale(y0 + y);
			});

    var color      = options.color;
    var colorScale = d3.scale.ordinal()
      .domain(_.map(data, options.name))
      .range(colors);
		if (!_.isFunction(color)) {
			color = _.flow(options.name, colorScale);
		}

		var slice = g.selectAll('.slice').data(pie(_.cloneDeep(data)));

		slice.enter()
			.append('path')
			.attr('class', 'slice');

		slice.attr({
			'd'    : arc,
			'fill' : color
		});

		slice.exit().remove();

    if (data.length > 1) {
      svg.select('.legend')
        .attr('transform', 'translate(' + (w + 4) +',0)')
        .call(legend().scale(colorScale));
    } else {
      svg.select('.legend').selectAll('g').remove();
    }
	}
});

module.exports = PieChart;
