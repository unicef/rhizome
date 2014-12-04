'use strict';

var d3   = require('d3');

var util = require('../../util/data');

module.exports = {
	paramAttributes: [
		'data-lines',
		'data-areas',
		'data-width',
		'data-height'
	],

	mixins: [
		require('./yGrid'),
		require('./xAxis')
	],

	data: function () {
		return {
			lines : [],
			areas : [],
			width : 100,
			height: 100
		};
	},

	created: function () {
		if (!this.$options.hasOwnProperty('x')) {
			this.$options.x = d3.time.scale();
		}

		if (!this.$options.hasOwnProperty('y')) {
			this.$options.y = d3.scale.linear();
		}
	},

	methods: {
		draw: function () {
			function getX(d) {
				return d.campaign.start_date;
			}

			function getY(d) {
				return d.value;
			}

			function getScaledX(d) {
				return x(getX(d));
			}

			function getScaledY(d) {
				return y(getY(d));
			}

			function defined(d) {
				return util.defined(getY(d));
			}

			var svg = d3.select(this.$el);

			var dataset = [this.lines, this.areas];
			var start   = util.min(dataset, getX);
			var end     = util.max(dataset, getX);
			var lower   = util.min(dataset, getY);
			var upper   = util.max(dataset, getY);

			var x = this.$options.x;
			var y = this.$options.y;

			x.domain([start, end])
				.range([0, this.width]);
			y.domain([lower, upper])
				.range([this.height, 0]);

			var area = d3.svg.area()
				.defined(defined)
				.x(getScaledX)
				.y(getScaledY);

			var areas = svg.selectAll('.area').data(this.areas);

			areas.enter().append('path')
				.attr('class', 'area');

			areas.attr({
				d: area
			});

			var line = d3.svg.line()
				.defined(defined)
				.x(getScaledX)
				.y(getScaledY);

			var lines = svg.selectAll('.line').data(this.lines);

			lines.enter().append('path')
				.attr('class', 'line');

			lines.attr({
				d: line
			});

			this._callHook('drawn');
		}
	},

	on: {
		'hook:attached': 'draw'
	},

	watch: {
		'lines' : 'draw',
		'areas' : 'draw',
		'width' : 'draw',
		'height': 'draw'
	}
};
