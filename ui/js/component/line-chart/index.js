'use strict';

var d3 = require('d3');

var x = d3.scale.linear(),
	y = d3.scale.linear(),
	line = d3.svg.line();

module.exports = {
	template: require('./template.html'),
	data: function () {
		return {
			margin: { top: 0, right: 0, bottom: 0, left: 0 },
			series: []
		};
	},
	ready: function () {
		// Trigger initial size calculation.
		this.handleEvent();

		// Update the element's size when the parent resizes.
		this.$el.parentElement.addEventListener('resize', this);

		// Update scales when the data series change.
		this.$watch('series', this.invalidateScale);
	},
	computed: {
		contentHeight: function () {
			return this.height - this.margin.top - this.margin.bottom;
		},
		contentWidth: function () {
			return this.width - this.margin.left - this.margin.right;
		},
	},
	filters: {
		line: function (v) {
			this.$log(v);
			return line(v);
		},
		x: x,
		y: y
	},
	methods: {
		handleEvent: function () {
			this.width = this.$el.parentElement.clientWidth;
			this.height = this.$el.parentElement.clientHeight;
		},
		invalidateScale: function () {
			x.domain(d3.extent(this.series, function (d) { return d.x; }));
			y.domain(d3.extent(this.series, function (d) { return d.x; }));
		},
		invalidateSize: function () {
			x.range([0, this.contentWidth]);
			y.range([this.contentHeight, 0]);
		}
	}
};
