'use strict';

var _  = require('lodash');
var d3 = require('d3');

var browser = require('util/browser');

var DEFAULTS = {
	aspect : 1
};

function ChoroplethMap() {}

_.extend(ChoroplethMap.prototype, {
	defaults : DEFAULTS,

	initialize : function (el, data, options) {
		options = this._options = _.defaults({}, options, DEFAULTS);

		var w = this._width = el.clientWidth;
		var h = w * options.aspect;

		var svg = this._svg = d3.select(el).append('svg')
			.attr('viewBox', '0 0 ' + w + ' ' + h);

		if (browser.isIE()) {
			svg.attr({
				'width'  : w,
				'height' : h
			})
		}

		svg.append('g').attr('class', 'data');

		this.update(data, options);
	},

	update : function (data, options) {
		options = _.assign(this._options, options);

		var svg = this._svg;
		var g   = svg.select('.data');
	}
});

module.exports = ChoroplethMap;
