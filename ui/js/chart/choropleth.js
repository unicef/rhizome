'use strict';

var _  = require('lodash');
var d3 = require('d3');

var browser = require('util/browser');

var DEFAULTS = {
	aspect : 1,
	domain : _.noop,
	margin : {
		top    : 0,
		right  : 0,
		bottom : 0,
		left   : 0
	},
	onClick     : _.noop,
	onMouseOver : _.noop,
	onMouseOut  : _.noop,
	value       : _.property('properties.value')
};

function _calculateBounds(features) {
	var lat = _.property(1);
	var lng = _.property(0);

	if (features.length < 1) {
		return [[0,0], [0,0]];
	}

	var coordinates = _(features).map(function (f) {
			return _.flatten(f.geometry.coordinates);
		})
		.flatten()
		.value();

	var left   = d3.min(coordinates, lng);
	var right  = d3.max(coordinates, lng);
	var bottom = d3.min(coordinates, lat);
	var top    = d3.max(coordinates, lat);

	return [[left, top], [right, bottom]];
}

function _calculateCenter(bounds) {
	var lat = bounds[1][1] + ((bounds[0][1] - bounds[1][1]) / 2);
	var lng = bounds[0][0] + ((bounds[1][0] - bounds[0][0]) / 2);

	return [lng, lat];
}

function ChoroplethMap() {}

_.extend(ChoroplethMap.prototype, {
	defaults : DEFAULTS,

	initialize : function (el, data, options) {
		options = this._options = _.defaults({}, options, DEFAULTS);

		var margin = options.margin;

		var w = this._width = el.clientWidth;
		var h = this._height = w * options.aspect;

		var svg = this._svg = d3.select(el).append('svg')
			.attr('class', 'reds')
			.attr('viewBox', '0 0 ' + w + ' ' + h);

		if (browser.isIE()) {
			svg.attr({
				'width'  : w,
				'height' : h
			});
		}

		var g = svg.append('g')
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

		g.append('g').attr('class', 'data');

		this.update(data);
	},

	update : function (data, options) {
		options = _.assign(this._options, options);

		var margin = options.margin;
		var w = this._width - margin.left - margin.right;
		var h = this._height - margin.top - margin.bottom;

		var svg = this._svg;
		var g   = svg.select('.data');

		var bounds = _calculateBounds(data);
		var center = _calculateCenter(bounds);

		var projection = d3.geo.conicEqualArea()
			.parallels([bounds[1][1], bounds[0][1]])
			.rotate([-center[0], 0])        // Rotate the globe so that the country is centered horizontally
			.center([0, center[1]])        // Set the center of the projection so that the polygon is moved vertically into the center of the viewport
			.translate([w / 2, h / 2]) // Translate to the center of the viewport
			.scale(1);

		var b = [projection(bounds[0]), projection(bounds[1])];
		var s = 1 / Math.max((b[1][0] - b[0][0]) / w, (b[1][1] - b[0][1]) / h);

		projection.scale(s);

		var path = d3.geo.path().projection(projection);

		var domain = options.domain(data);

		if (!_.isArray(domain)) {
			domain    = d3.extent(data, options.value);
			domain[0] = d3.min(domain[0], 0);
		}

		var quantize = d3.scale.quantize()
			.domain(domain)
			.range(d3.range(1, 7));

		var region = g.selectAll('.region')
			.data(data, function (d, i) { return _.get(d, 'properties.region_id', i); });

		region.enter().append('path');

		region.attr({
				'd'     : path,
				'class' : function (d) {
					var v = options.value(d);
					var classNames = ['region'];

					if (_.isFinite(v)) {
						classNames.push('clickable');
						classNames.push('q-' + quantize(v));
					}

					return classNames.join(' ');
				}
			})
			.on('click', function (d) {
				options.onClick(d, this);
			})
			.on('mouseover', function (d) {
				options.onMouseOver(d, this);
			})
			.on('mouseout', function (d) {
				options.onMouseOut(d, this);
			});

		region.exit().remove();
	}
});

module.exports = ChoroplethMap;
