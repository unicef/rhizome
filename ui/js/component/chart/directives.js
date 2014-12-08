/**
 * @module component/chart/directives
 */

'use strict';

var d3 = require('d3');

module.exports = {
	/**
	 * Create a new filter on a component for a given scale type.
	 *
	 * Arguments are used as the filter names (be careful, you can overwrite
	 * existing filters this way) and expressions are used to look up the scale
	 * type on `d3.scale`.
	 *
	 * Example:
	 *    v-scale="x: linear, y: log"
	 */
	scale: {
		isLiteral: true,

		bind: function () {
			this.vm.$filters[this.arg] = d3.scale[this.expression]();
		}
	},

	/**
	 * Set the domain on scale filter.
	 *
	 * Example:
	 *     v-domain="x: [10, 20], y: [0, yMax]"
	 */
	domain: {
		acceptStatement: true,

		update: function (value) {
			this.vm.$filters[this.arg].domain(value);
		}
	},

	/**
	 * Set the range on a scale filter.
	 *
	 * Example:
	 *     v-range="x: [0, 10], y: [height, 0]"
	 */
	range: {
		acceptStatement: true,

		update: function (value) {
			this.vm.$filters[this.arg].range(value);
		}
	}
};
