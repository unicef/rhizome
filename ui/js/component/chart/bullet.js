'use strict';

var d3 = require('d3');

module.exports = {
	paramAttributes: [
		'width',
		'height',
		'scale'
	],

	data: function () {
		return {
			scale : 'linear',
			width : 100,
			height: 100,
			value : 0,
			marker: 0,
			ranges: [{
				name : '',
				start: 0,
				end  : 1
			}]
		};
	},

	methods: {
		draw: function () {
			if (!this.ranges || !this.value || !this.marker) {
				return;
			}

			var svg = d3.select(this.$el);

			var x = d3.scale.linear()
				.domain([0, d3.max(this.ranges, function (d) { return d.end; })])
				.range([0, this.width]);

			var bg = svg.select('.ranges').selectAll('.range')
				.data(this.ranges);

			bg.enter().append('rect').attr('class', 'range');

			bg.attr({
				height: this.height,
				width : function (d) { return x(d.end - d.start); },
				x     : function (d) { return x(d.start); }
			}).style('fill', '#fff');

			bg.exit().remove();

			svg.select('.marker').attr({
				height: this.height * 3 / 4,
				width : this.width / 20,
				y     : this.height / 8,
				x     : x(this.marker)
			});

			svg.select('.value').attr({
				height: this.height / 2,
				width : x(this.value),
				y     : this.height / 4
			});
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
