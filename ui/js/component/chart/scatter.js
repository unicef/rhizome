'use strict';

var _  = require('lodash');
var d3 = require('d3');

function x(d) {
	return d.x;
}

function y(d) {
	return d.y;
}

module.exports = {

	template: require('./chart.html'),
	replace : true,

	paramAttributes: [
		'data-x',
		'data-y'
	],

	mixins: [
		require('component/chart/mixin/margin'),
		require('component/chart/mixin/resize'),
		require('component/chart/mixin/with-indicator')
	],

	data: function () {
		return {
			campaign    : null,
			indicators  : [],
			marginLeft  : 24,
			marginBottom: 24,
			region      : null,
			x           : null,
			y           : null
		};
	},

	computed: {
		query: function () {
			return {
				indicator__in: _.map(this.indicators, function (d) {
					return d.id || d;
				}),

				campaign_start: this.campaign.end,
				campaign_end  : this.campaign.end,
				parent_region: this.region,
				level        : 'province'
			};
		},

		series: function () {
			if (this.empty) {
				return [];
			}

			var xProp = this.x;
			var yProp = this.y;

			return _(this.datapoints)
				.groupBy('region')
				.map(function (d, region) {
					var indicators = _.indexBy(d, 'indicator');

					var isDefined = indicators.hasOwnProperty(xProp) &&
						indicators.hasOwnProperty(yProp);

					return isDefined ? {
						id  : region,
						name: region,
						x   : indicators[xProp].value,
						y   : indicators[yProp].value
					} : null;
				})
				.filter(function (d) {
					return d !== null;
				})
				.value();
		},

		xScale: function () {
			var domain = this.domain || [];

			if (domain.length < 2) {
				var datapoints = this.series;

				domain[0] = Math.min(0, d3.min(datapoints, x)) || 0;
				domain[1] = d3.max(datapoints, x) || domain[0] + 1;
			}

			var scale = d3.scale.linear()
				.domain(domain)
				.range([0, this.contentWidth]);

			return scale;
		},

		yScale: function () {
			var domain = this.range || [];

			if (domain.length < 2) {
				var datapoints = this.series;

				domain[0] = Math.min(0, d3.min(datapoints, y)) || 0;
				domain[1] = d3.max(datapoints, y) || domain[0] + 1;
			}

			var scale = d3.scale.linear()
				.domain(domain)
				.range([this.contentHeight, 0]);

			return scale;
		}
	},

	methods: {
		draw: function () {
			function cx(d) {
				return xScale(x(d));
			}

			function cy(d) {
				return yScale(y(d));
			}

			var svg    = d3.select(this.$el);
			var xScale = this.xScale;
			var yScale = this.yScale;

			var point = svg
				.select('.data')
				.selectAll('.point')
				.data(this.series, function (d, i) {
					return d.id || i;
				});

			// FIXME: Hard-coded transition speed
			point
				.transition()
				.duration(500)
				.attr({
					'cx': cx,
					'cy': cy
				});

			// FIXME: Hard-coded transition speed
			point.enter()
				.append('circle')
				.attr({
					'class': 'point',
					'cx'   : cx,
					'cy'   : cy,
					'r'    : 0
				})
				.on({
					'mouseover': this.showTooltip,
					'mouseout' : this.hideTooltip
				})
				.transition()
				.duration(500)
				.attr('r', 2);

			// FIXME: Hard-coded transition speed
			point.exit()
				.transition()
				.duration(500)
				.attr('r', 0)
				.remove();

			var xAxis = d3.svg.axis()
				.scale(xScale)
				.orient('bottom');

			svg
				.select('.x.axis')
				.call(xAxis);

			var yAxis = d3.svg.axis()
				.scale(yScale)
				.orient('left');

			svg
				.select('.y.axis')
				.call(yAxis);
		}
	},

	watch: {
		'datapoints': 'draw',
		'width'     : 'draw',
		'height'    : 'draw'
	}
};
