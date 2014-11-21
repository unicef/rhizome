'use strict';

var d3 = require('d3');

module.exports = {
	data: function () {
		return {
			datapoints: [],
			d: ''
		};
	},

	beforeCompile: function () {
		var x = this.$options.filters.x;
		var y = this.$options.filters.y;

		this.$options.filters.line = d3.svg.line()
			.x(function (d) { return x(d.x); })
			.y(function (d) { return y(d.y); });

		this.$options.filters.area = d3.svg.area()
			.x(function (d) { return x(d.x); })
			.y0(function () { return y(0); })
			.y1(function (d) { return y(d.y); });
	},

	ready: function () {
		this.invalidateDisplay();
		this.$on('invalidateDisplay', this.invalidateDisplay);
	},

	methods: {
		invalidateDisplay: function () {
			this.datapoints.__ob__.notify();
		}
	}
};
