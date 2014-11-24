'use strict';

var d3  = require('d3');

module.exports = {
	data: function () {
		return {
			slice: {},
			radius: {
				inner: 0,
				outer: 100
			}
		};
	},

	ready: function () {
		this.$watch('radius', function () {
			this.slice.__ob__.notify();
		}, true);
	},

	filters: {
		arc: function (value) {
			var arc = d3.svg.arc()
				.innerRadius(this.radius.inner)
				.outerRadius(this.radius.outer);

			return arc(value);
		}
	},

	directives: {
		radius: {
			isLiteral: true,

			bind: function () {
				this.vm.$data.radius[this.arg] = this.expression;
			}
		}
	},
};
