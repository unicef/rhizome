/**
 * @module component/chart/pie
 */
'use strict';

var d3 = require('d3');

module.exports = {
	replace : true,
	template: require('./pie.html'),

	data: function () {
		return {
			data  : [],
			radius: {
				inner: 0,
				outer: 100,
			},
			angle: {
				start: 0,
				end  : 2 * Math.PI
			},
			value: null
		};
	},

	computed: {
		arcs: function () {
			// Place the value property name in scope so it's accessible inside closures.
			var value = this.value;

			// Rebuild the pie layout every time so that the arcs property is bound to
			// all its radius and angle dependencies.
			var pie = d3.layout.pie()
				.value(function (d) { return value ? d[value] : d; })
				.innerRadius(this.radius.inner)
				.outerRadius(this.radius.outer)
				.startAngle(this.angle.start)
				.endAngle(this.angle.end);

			return pie(this.data);
		}
	},

	filters: {
		/**
		 * Returns a string of path commands for an SVG `d` attribute.
		 *
		 * @arg {Object} value - object containing startAngle and endAngle
		 *	properties (in radians)
		 */
		arc: function (value) {
			var arc = d3.svg.arc()
				.innerRadius(this.radius.inner)
				.outerRadius(this.radius.outer);

			return arc(value);
		}
	},

	directives: {
		/**
		 * Set a property on the radius object.
		 *
		 * The argument is used as the property name on the radius object, so it is
		 * possible to create new properties on the radius object for use within
		 * the template.
		 *
		 * Example:
		 *    v-radius="inner: 5, outer: 10"
		 */
		radius: {
			acceptStatement: true,

			update: function (value) {
				this.vm.radius[this.arg] = value;
			}
		},

		/**
		 * Set a property on the angle object.
		 *
		 * The argument is used as the property name on the angle object, so it is
		 * possible to create new properties on the angle object for use within
		 * the template.
		 *
		 * Example:
		 *    v-angle="start: 0, end: Math.PI"
		 */
		angle: {
			acceptStatement: true,

			update: function (value) {
				this.vm.angle[this.arg] = value;
			}
		}
	}
};
