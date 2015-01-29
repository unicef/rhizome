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

			function fill(value, marker, ranges) {
				// FIXME: Hack for getting fill colors for good and bad performance.
				// This should probably be encapsulated outside of this chart, applied
				// to the VM before it is rendered, and the chart should just read a
				// color property
				var delta = value - marker;

				if (delta > 0.25) {
					return '#2B8CBE';
				}

				if (delta < 0) {
					return '#AF373E';
				}

				for (var i = ranges.length - 1; i >= 0; i--) {
					var range = ranges[i];

					if (range.start <= value && range.end > value && range.name === 'bad') {
						return '#AF373E';
					}
				}

				return '#707677';
			}

			if (!this.ranges) {
				this._data.ranges = [];
			}

			var svg    = d3.select(this.$el);
			var height = this.height || 0;
			var width  = this.width || 0;

			var x = d3.scale.linear()
				.domain([0, d3.max(this.ranges, function (d) { return d.end; })])
				.range([0, width]);

			// FIXME: color scale shouldn't be hard-coded. It should be generated
			// according to the number of qualitative ranges and not depend on the
			// ranges being "good," "bad," and "ok."
			var color = d3.scale.ordinal()
				.domain(['bad', 'ok', 'good'])
				.range(['#B3B3B3', '#CCCCCC', '#E6E6E6']);

			var bg = svg.select('.ranges').selectAll('.range')
				.data(this.ranges);

			bg.enter().append('rect').attr('class', 'range');

			bg.attr({
				height: height,
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
				y: height
			})
				.style('font-size', height / 6)
				.text(function (d) { return d.name; });

			labels.exit().remove();

			var fillColor = fill(this.value, this.marker, this.ranges);

			svg.select('.marker').attr({
				height: height * 3 / 4,
				width : this.markerWidth,
				y     : height / 8,
				x     : x(this.marker) || 0
			}).style({
				display: display(this.marker),
				fill: fillColor
			});

			svg.select('.value').attr({
				height: height / 2,
				width : x(this.value) || 0,
				y     : height / 4
			}).style({
				display: display(this.value),
				fill: fillColor
			});

			var format = d3.format('%');

			svg.select('.label').attr({
				y: height / 2,
				dy: height / 8,
			}).style({
				'font-size': height / 4,
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
