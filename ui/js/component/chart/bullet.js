'use strict';

var _        = require('lodash');
var d3       = require('d3');
var moment   = require('moment');

var util     = require('../../util/data');
var dateUtil = require('../../util/date');
var api      = require('../../data/api');

function campaignComparator(a, b) {
	return (a.campaign.start_date < b.campaign.start_date) ? -1 :
		(a.campaign.start_date > b.campaign.start_date) ? 1 : 0;
}

module.exports = {
	replace : true,
	template: require('./bullet.html'),

	paramAttributes: [
		'data-marker-width',
		'data-indicator',
		'data-period'
	],

	mixins: [
		require('./resize')
	],

	partials: {
		'loading-overlay': require('./partials/loading-overlay.html')
	},

	data: function () {
		return {
			datapoints : [],
			markerWidth: 3,
			loading    : false,
			error      : false,
			period     : null,
			indicator  : null
		};
	},

	computed: {

		length: function () {
			var datapoints = this.datapoints;

			return (datapoints && datapoints.length) || 0;
		},

		value: function () {
			var length = this.length;

			if (length < 1) {
				return null;
			}

			return this.datapoints[length - 1].value;
		},

		marker: function () {
			console.info('bullet::marker', this.indicator.id);
			var length = this.length;

			if (length < 2) {
				console.info('bullet::marker', 'Not enough data points');
				return null;
			}

			var datapoints = this.datapoints;
			var avg        = 0;

			for (var i = length - 2; i >= 0; i--) {
				avg += datapoints[i].value;
			}

			console.debug('bullet::marker', 'sum', avg);

			avg /= (length - 1);

			console.debug('bullet::marker', 'length', length);
			console.debug('bullet::marker', 'average', avg);

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

		title: function () {
			if (!this.indicator) {
				return '';
			}

			return this.indicator.short_name || '';
		}

	},

	methods: {

		load: function () {
			console.info('bullet::load');
			if (!this.indicator || !this.region || !this.campaign) {
				return;
			}

			console.debug('bullet::load', 'indicator', this.indicator, 'region', this.region, 'campaign', this.campaign);

			this.loading = true;

			var q = {
				campaign_end : this.campaign.end,
				indicator__in: [this.indicator.id],
				region__in   : [this.region]
			};

			if (this.period) {
				var start = moment(this.campaign.date, 'YYYYMMDD');

				q.campaign_start = start.subtract.apply(
						start,
						dateUtil.parseDuration(this.period)
					).format('YYYY-MM-DD');
			}

			console.debug('bullet::load', 'query', q);

			api.datapoints(q).then(this.parseData, this.dataError);
		},

		draw: function () {
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

			var svg    = d3.select(this.$el).select('.bullet');
			var height = this.height || 0;
			var width  = this.width || 0;

			var x = d3.scale.linear()
				.domain([0, this.max])
				.range([0, width]);

			var ranges = (this.indicator && this.indicator.ranges) || [];

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

			var fillColor = fill(this.value, this.marker, ranges);

			var value = svg.selectAll('.value')
				.data(this.value ? [this.value] : []);

			value.transition().duration(300)
				.style('fill', fillColor);

			value.enter().append('rect')
				.attr({
					'class': 'value',
					'width': 0
				})
				.style('fill', fillColor);

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

			var format = d3.format(this.formatString) ||
				this.indicator.format ||
				String;

			var label = svg.selectAll('.label')
				.data(this.value ? [this.value] : []);

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
				.transition().duration(300)
					.tween('text', function (d) {
						// FIXME: We should generalize this text tween and decide between
						// rounded and regular interpolation based on whether or not there
						// is a fractional component to any of the numbers.
						var i = d3.interpolateRound(Number(this.textContent), d);

						return function (t) {
							this.textContent = format(i(t));
						};
					});

			label.exit()
				.transition().duration(300)
					.style('opacity', 0)
				.remove();

			var marker = svg.selectAll('.marker')
				.data(this.marker ? [this.marker] : []);

			marker.transition().duration(300)
				.style('fill', fillColor);

			marker.enter().insert('rect', '.label')
				.attr({
					'class': 'marker',
					'x'    : 0
				})
				.style('fill', fillColor);

			marker.attr({
				'height': height * 3 / 4,
				'width' : this.markerWidth,
				'y'     : height / 8
			})
				.transition().duration(300)
					.attr('x', d3.scale.linear()
						.domain([0, this.max])
						.range([0, this.width - this.markerWidth]));

			marker.exit()
				.transition().duration(300)
					.attr('width', 0)
				.remove();
		},

		parseData: function (data) {
			var indicator = this.indicator.id;

			data.objects.forEach(function (d) {
				var indicators = _.indexBy(d.indicators, 'indicator');

				d.value = indicators[indicator].value;
			});

			// Keep data sorted by campaign start date so that it's easier to
			// compute the historical average.
			data.objects.sort(campaignComparator);

			this.loading    = false;
			this.datapoints = data.objects;
		},

		dataError: function (err) {
			console.log(err);

			this.loading = false;
			this.error   = true;
		},

		loadIndicator: function () {
			console.info('bullet::indicator', 'watch');
			console.debug('bullet::indicator', this.indicator);

			var self = this;

			if (!this.indicator) {
				return;
			}

			if (_.isNumber(this.indicator) || _.isString(this.indicator)) {
				api.indicators({ id: this.indicator })
					.then(function (data) {
						self.indicator = data.objects[0];
					}, this.dataError);
			} else {
				self.load();
			}
		}
	},

	events: {
		'hook:created': 'loadIndicator'
	},

	watch: {
		'campaign'  : 'load',
		'period'    : 'load',
		'region'    : 'load',

		'datapoints': 'draw',
		'height'    : 'draw',
		'width'     : 'draw',

		'indicator' : 'loadIndicator'
	}
};
