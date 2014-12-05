'use strict';

var d3   = require('d3');
var util = require('../../util/data');

module.exports = {
	replace : true,
	template: require('./bullet.html'),

	paramAttributes: [
		'width',
		'height',
		'data-scale',
		'data-marker-width'
	],

	data: function () {
		return {
			scale      : 'linear',
			width      : 100,
			height     : 100,
			value      : 0,
			marker     : 0,
			markerWidth: 3,
			ranges     : [{
				name : '',
				start: 0,
				end  : 1
			}]
		};
	},

	methods: {
		draw: function () {
			function display(d) {
				return util.defined(d) ?
					'default' :
					'none';
			}

			if (!this.ranges) {
				this._data.ranges = [];
			}

			var svg = d3.select(this.$el);

			var x = d3.scale.linear()
				.domain([0, d3.max(this.ranges, function (d) { return d.end; })])
				.range([0, this.width]);

			var color = d3.scale.ordinal()
				.domain(['bad', 'ok', 'good'])
				.range(['#B3B3B3', '#CCCCCC', '#E6E6E6']);

			var bg = svg.select('.ranges').selectAll('.range')
				.data(this.ranges);

			bg.enter().append('rect').attr('class', 'range');

			bg.attr({
				height: this.height,
				width : function (d) { return x(d.end - d.start); },
				x     : function (d) { return x(d.start); }
			}).style('fill', function (d) {
				return color(d.name);
			});

			bg.exit().remove();

			var labels = svg.select('.ranges').selectAll('.range-label')
				.data(this.ranges);

			labels.enter().append('text')
				.attr({
					'class': 'range-label',
					'dy': -3,
					'dx': 2
				});

			labels.attr({
				x: function (d) { return x(d.start); },
				y: this.height
			})
				.style('font-size', this.height / 6)
				.text(function (d) { return d.name; });

			labels.exit().remove();

			svg.select('.marker').attr({
				height: this.height * 3 / 4,
				width : this.markerWidth,
				y     : this.height / 8,
				x     : x(this.marker)
			}).style({
				display: display(this.marker)
			});

			svg.select('.value').attr({
				height: this.height / 2,
				width : x(this.value),
				y     : this.height / 4
			}).style({
				'display': display(this.value)
			});

			var format = d3.format('%');

			svg.select('.label').attr({
				y: this.height / 2,
				dy: this.height / 8,
			}).style({
				'font-size': this.height / 4,
				'display': display(this.value)
			})
				.text(format(this.value));
		}
	},

	on: {
		'hook:attached': 'draw',
	},

	watch: {
		'width' : 'draw',
		'height': 'draw',
		'value' : 'draw',
		'marker': 'draw',
		'ranges': 'draw'
	}
};
