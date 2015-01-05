'use strict';

var _    = require('lodash');
var d3   = require('d3');

var util = require('../../util/data');

module.exports = {
	created: function () {
		function getAnnotationLayer() {
			var svg = d3.select(self.$el).selectAll('.annotations').data([0]);

			svg.enter().append('g')
				.attr('class', 'annotations');

			return svg;
		}

		function getLast(series) {
			var o = null;
			var x = -Infinity;

			for (var i = series.points.length - 1; i >= 0; i--) {
				var p = series.points[i];

				if (p.x > x && util.defined(p.value)) {
					x = p.x;
					o = { datum: p };

					if (series.name) {
						o.name = series.name;
					}
				}
			}

			return o;
		}

		function makeLabel(g) {
			var yFmt = self.yFmt || Object;

			g.each(function (d) {
				var g = d3.select(this);

				g.attr('transform', function (d) {
					return 'translate(' + self.x(d.datum.x) + ',' + self.y((d.datum.y0 || 0) + d.datum.y) + ')';
				});

				g.selectAll('text').remove();

				var value = g.append('text')
					.attr({
						'text-anchor': 'end',
					})
					.text(yFmt(d.datum.value));

				if (d.name) {
					value.attr('dy', '1.1em');

					g.append('text')
						.attr({
							'text-anchor': 'end',
							'dy'         : '-.2em'
						})
						.text(d.name);
				}
			});
		}

		var self = this;

		this.$on('hook:drawn', function () {
			var svg    = getAnnotationLayer();
			var series = this.series || [];
			var data   = series.map(getLast)
				.filter(function (d) { return d !== null; });
			var label  = svg.selectAll('.label').data(data);

			label.enter().append('g').attr('class', 'label');

			label.call(makeLabel);
		});

		this.$on('show-annotation', function (d) {
			var svg = getAnnotationLayer();

			svg.selectAll('.label')
				.transition().duration(300)
					.style('opacity', '0');

			var annotated = Array.prototype.concat.apply([],
				_.map(this.series, function (s) {
					var match = [];

					for (var i = s.points.length - 1; i >= 0; i--) {
						if (s.points[i].x === d.x) {
							var o = {
								datum: s.points[i]
							};

							if (s.name) {
								o.name = s.name;
							}

							match.push(o);
						}
					}

					return match;
				}));

			var label = svg.selectAll('.temp.label').data(annotated);

			label.enter().append('g').attr('class', 'temp label')
				.style('opacity', '0');

			label.call(makeLabel);

			label.transition().duration(300)
					.style('opacity', '1');
		});

		this.$on('hide-annotation', function () {
			var svg = getAnnotationLayer();

			svg.selectAll('.label')
				.transition().duration(300)
					.style('opacity', '1');

			svg.selectAll('.temp.label')
				.transition().duration(300)
					.style('opacity', '0')
					.remove();
		});
	},
};
