/* global window */
'use strict';

var _   = require('lodash');
var d3  = require('d3');
var dom = require('../../util/dom');

module.exports = {
	template: require('./template.html'),
	replace: true,

	paramAttributes: [
		'aspect'
	],

	data: function () {
		return {
			margin: {
				top   : 0,
				right : 0,
				bottom: 0,
				left  : 0
			},
			series: [],
			width : 200,
			xTicks: [],
			yTicks: []
		};
	},

	created: function () {
		this.$options.filters.x = d3.scale.linear();
		this.$options.filters.y = d3.scale.linear();
	},

	ready: function () {
		window.addEventListener('resize', this);
		this.handleEvent();
	},

	computed: {
		contentWidth: function () {
			var left  = this.margin.left || 0;
			var right = this.margin.right || 0;

			return this.width - left - right;
		},

		contentHeight: function () {
			var top    = this.margin.top || 0;
			var bottom = this.margin.bottom || 0;

			return this.height - top - bottom;
		},

		domain: {
			get: function () {
				return this.$options.filters.x.domain();
			},

			set: function (value) {
				this.$options.filters.x.domain(value);
				this.invalidateTicks();
			}
		},

		height: function () {
			return this.width / (this.aspect || 1);
		},

		range: {
			get: function () {
				return this.$options.filters.y.domain();
			},

			set: function (value) {
				this.$options.filters.y.domain(value);
				this.invalidateTicks();
			}
		},

		transform: function () {
			return 'translate(' + this.margin.left + ',' + this.margin.top + ')';
		}
	},

	methods: {
		handleEvent: function () {
			var content = dom.contentArea(this.$el.parentElement);

			this.$data.width = content.width;
		},

		invalidateTicks: function () {
			var x = this.$options.filters.x;
			var y = this.$options.filters.y;

			x.range([0, this.contentWidth]);
			y.range([this.contentHeight, 0]);

			this.yTicks = y.ticks().map(function (tick) {
				return {
					position: y(tick),
					label   : tick
				};
			});

			this.xTicks = x.ticks().map(function (tick) {
				return {
					position: x(tick),
					label   : tick
				};
			});

			this.$broadcast('invalidateDisplay');
		}
	},

	watch: {
		'series': function () {
			var data = _.reduce(this.series, function (combined, s) {
				return combined.concat(s);
			}, []);

			this.domain = d3.extent(data, function (d) { return d.x; });
			this.range  = d3.extent(data, function (d) { return d.y; });
		},

		'height': 'invalidateTicks',
		'width' : 'invalidateTicks'
	}
};
