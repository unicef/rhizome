/**
 * @module component/chart/filters
 */

'use strict';

var _  = require('lodash');
var d3 = require('d3');

module.export = {

	/**
	 * Returns a string representing a translation for the svg translate property.
	 *
	 * @param {Object} value - the value passed to the filter from the template
	 * @param {string|number} [x=0[ - the property name to access on `value` for
	 *	the x translation, or the value to use for the x translation
	 * @param {string|number} [y=0] - the property name to access on `value for
	 *	the y translation, or the value to use for the y translation
	 */
	translate: function (value, x, y) {
		x = x || 0;
		y = y || 0;

		var dx = _.isUndefined(value[x]) ? x : value[x];
		var dy = _.isUndefined(value[y]) ? y : value[y];

		return 'translate(' + dx + ',' + dy + ')';
	},

	min: function (value, keypath) {
		return d3.min(value, function (d) {
			return keypath ? d.$get(keypath) : Number(d);
		});
	},

	max: function (value, keypath) {
		return d3.max(value, function (d) {
			return keypath ? d.$get(keypath) : Number(d);
		});
	}
};
