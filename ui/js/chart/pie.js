'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var browser = require('util/browser');
var colors  = require('colors');

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
	value : _.property('value')
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

		this.update(data);
	},

	update : function (data, options) {
		options = _.assign(this._options, options);
		var margin = options.margin;

		data = data || [];

		var w = this._width - margin.left - margin.right;
		var h = this._height - margin.top - margin.bottom;
		var s = Math.min(w, h);

		var svg = this._svg;

		svg.attr('viewBox', '0 0 ' + this._width + ' ' + this._height)
			.select('.margin')
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

		if (browser.isIE()) {
			svg.attr({
				'width'  : this._width,
				'height' : this._height
			});
		}

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

		var getIndex = function (d, i) { return i; };

		var scale = d3.scale.linear()
			.domain(options.domain(data, options))
			.range([0, 2 * Math.PI]);

		var pie = d3.layout.stack()
			.values (function (d) { return [d]; })
			.x(getIndex)
			.y(options.value)
			.out(function (d, y0, y) {
				d.startAngle = scale(y0);
				d.endAngle   = scale(y);
			});

		var color = options.color;
		if (!_.isFunction(color)) {
			color = _.flow(getIndex, d3.scale.ordinal().range(colors));
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
	}
});

module.exports = PieChart;
