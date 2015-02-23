'use strict';

var _  = require('lodash');
var d3 = require('d3');
var moment = require('moment');

module.exports = {
	replace : true,
	template: require('./bullet.html'),

	paramAttributes: [
		'data-marker-width',
	],

	mixins: [
		require('./mixin/resize'),
		require('./mixin/with-indicator')
	],

	partials: {
		'loading-overlay': require('./partial/loading-overlay.html')
	},

	data: function () {
		return {
			markerWidth : 3,
			formatString: '%'
		};
	},

	computed: {
		delta: function () {
			return (this.value - this.marker);
		},

		status: function () {
			var delta = this.delta;

			if (_.isNaN(delta)) {
				return '';
			}

			if (delta < 0 || (this.value <= 0 && this.value !== null)) {
				return 'down';
			}

			return delta >= 0.25 ? 'up' : '';
		},

		value: function () {
			var length = this.length;

			if (length < 1) {
				return null;
			}

			for (var i = 0, l = this.datapoints.length; i < l; i++) {
				var d = this.datapoints[i];
				if (moment(d.campaign.start_date).format('YYYYMMDD') === this.campaign.date) {
					return d.value;
				}
			}

			return null;
		},

		marker: function () {
			var length = this.length;

			if (length < 2) {
				return null;
			}

			var datapoints = this.datapoints;
			var avg        = 0;
			var l          = 0;

			for (var i = length - 1; i >= 0; i--) {
				if (!_.isNull(datapoints[i].value) && !_.isUndefined(datapoints[i].value)) {
					avg += datapoints[i].value;
					l++;
				}
			}

			avg /= l;

			return avg;
		},

		max: function () {
			if (this.length < 1 || !this.indicator) {
				return 0;
			}

			var ranges = this.indicator.ranges || [{ end: 0 }];

			return Math.max(d3.max(ranges, function (d) { return d.end; }),
				d3.max(this.datapoints, function (d) { return d.value; }));
		},

		indicator: function () {
			var indicators = this.indicators;

			return (indicators && indicators.length > 0) ? indicators[0] : null;
		},

		title: function () {
			if (!this.indicator) {
				return '';
			}

			return this.indicator.short_name || '';
		}

	},

	methods: {

		draw: function () {
			var svg    = d3.select(this.$el).select('.bullet');
			var height = 100;
			var width  = 318;

			var x = d3.scale.linear()
				.domain([0, 1])
				.range([0, width]);

			var ranges = (this.indicator && this.indicators.ranges) || [];

			var color = d3.scale.quantize()
				.domain(ranges.map(function (r) { return r.name; }))
				.range(['#B3B3B3', '#E6E6E6']);

			var bg = svg.select('.ranges').selectAll('.range')
				.data(ranges);

			bg.enter().append('rect').attr('class', 'range');

			bg.attr('height', height)
				.transition().duration(300)
					.attr({
						'width': function (d) { return x(d.end - d.start); },
						'x'    : function (d) { return x(d.start); }
					}).style('fill', function (d) {
						return color(d.name);
					});

			bg.exit().remove();

			var labels = svg.select('.ranges').selectAll('.range-label')
				.data(ranges);

			labels.enter().append('text')
				.attr({
					'class': 'range-label',
					'dy'   : -3,
					'dx'   : 2
				});

			labels.attr({
				'x': function (d) { return x(d.start); },
				'y': height
			})
				.style('font-size', height / 6)
				.text(function (d) { return d.name; });

			labels.exit().remove();

			var missing = _.isNull(this.value) || _.isUndefined(this.value);
			var value = svg.selectAll('.value')
				.data(missing ? [] : [this.value]);

			value.enter().append('rect')
				.attr({
					'class': 'value',
					'width': 0
				});

			value.attr({
					'height': height / 2,
					'y'     : height / 4
				})
				.transition().duration(300)
					.attr('width', x);

			value.exit()
				.transition().duration(300)
					.style('opacity', 0)
				.remove();

			var format = this.formatString ?
				d3.format(this.formatString) :
				this.indicator.format || String;

			var label = svg.selectAll('.label')
				.data(missing ? [] : [this.value]);

			label.enter().append('text')
				.attr({
					'class': 'label',
					'dx'   : 2
				}).text(0);

			label.attr({
					'y' : height / 2,
					'dy': height / 8,
				})
				.style({
					'font-size': height / 4,
				})
				.text(function (d) {
					return format(d);
				});

			label.exit()
				.transition().duration(300)
					.style('opacity', 0)
				.remove();

			var marker = svg.selectAll('.marker')
				.data(this.marker ? [this.marker] : []);

			marker.transition().duration(300);

			marker.enter().insert('rect', '.label')
				.attr({
					'class': 'marker',
					'x'    : 0
				});

			marker.attr({
				'height': height * 3 / 4,
				'width' : this.markerWidth,
				'y'     : height / 8
			})
				.transition().duration(300)
					.attr('x', d3.scale.linear()
						.domain(x.domain())
						.range([0, (width - this.markerWidth)]));

			marker.exit()
				.transition().duration(300)
					.attr('width', 0)
				.remove();
		}

	},

	watch: {
		'datapoints': 'draw',
		'height'    : 'draw',
		'width'     : 'draw',
	}
};
