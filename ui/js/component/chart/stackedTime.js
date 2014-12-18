'use strict';

var d3       = require('d3');

var coolgray = require('../../colors/coolgray');
var util     = require('../../util/data');

module.exports = {
	replace: true,

	mixins: [
		require('./hover-tiles'),
		require('./xAxis'),
		require('./yGrid')
	],

	data: function () {
		return {
			series: [],
			x     : d3.scale.linear(),
			y     : d3.scale.linear()
		};
	},

	methods: {
		draw: function () {
			function getX(d) {
				return d.x;
			}

			function getY(d) {
				return d.y0 + d.y;
			}

			function getValues(d) {
				return d.points;
			}

			function defined(d) {
				return util.defined(getY(d));
			}

			if (!this.series) {
				this.$set('series', []);
			}

			var svg = d3.select(this.$el);

			var stack = d3.layout.stack()
				.x(getX)
				.values(getValues);

			var layers  = stack(this.series);

			var dataset = this.series.map(getValues);
			var start   = new Date(util.min(dataset, getX));
			var end     = new Date(util.max(dataset, getX));
			var lower   = Math.min(0, util.min(dataset, function (d) { return d.y0; }));
			var upper   = util.max(dataset, getY);

			var x = this.x
				.domain([start, end])
				.range([0, this.width]);

			var y = this.y
				.domain([lower, upper])
				.range([this.height, 0]);

			var color = d3.scale.ordinal()
				.domain([0, this.series.length])
				.range(coolgray);

			var area = d3.svg.area()
				.defined(defined)
				.x(function (d) { return x(getX(d)); })
				.y0(function (d) { return y(d.y0); })
				.y1(function (d) { return y(getY(d)); });

			var paths = svg.select('.layers').selectAll('.layer')
				.data(layers);

			paths.enter().append('path')
				.attr('class', 'layer');

			paths.attr('d', function (d) { return area(getValues(d)); })
				.style('fill', function (d, i) { return color(i); });

			paths.exit().remove();

			this.$emit('chart-drawn', {
				el    : this.$el,
				series: dataset,
				x     : x,
				y     : y
			});

			this._callHook('drawn');
		}
	},

	on: {
		'hook:attached': 'draw'
	},

	watch: {
		'series': 'draw',
		'width' : 'draw',
		'height': 'draw'
	}
};
