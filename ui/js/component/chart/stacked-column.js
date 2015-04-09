'use strict';

var _  = require('lodash');
var d3 = require('d3');

var column  = require('./renderer/column');
var data    = require('util/data');
var label   = require('./renderer/label');
var palette = require('colors/coolgray');

// Color palette from I Want Hue
// var palette = [
// "#6094BA",
// "#699CA7",

// "#B6DAE5",
// "#589EE4",
// "#3CA6A9",
// "#909A92",

// "#D5D5C6",
// "#90D7D0",
// "#5CB3DE",
// "#A2B6C8",
// "#D2F2EA",
// "#8ED0E9"];

module.exports = {
	replace  : true,
	template : require('./bar.html'),

	paramAttributes : [
		'data-facet',
		'data-format-string',
		'data-x'
	],

	mixins : [
		require('./mixin/resize'),
		require('./mixin/margin'),
		require('./mixin/with-indicator')
	],

	data : function () {
		return {
			facet        : 'indicator.id',
			formatString : 's'
		};
	},

	computed : {
		empty : function () {
			return !this.datapoints || !this.datapoints.length;
		},

		series : function () {
			if (this.empty) {
				return [];
			}

			var x = this.x;

			if (_.isString(x)) {
				x = data.accessor(x);
			}

			var stack = d3.layout.stack()
				.offset('zero')
				.values(function (d) { return d.values; })
				.x(x)
				.y(function (d) { return d.value; });

			var indicators = _.indexBy(this.indicators, 'id');

			var series = _(this.datapoints)
				.groupBy(function (d) { return d.indicator; })
				.map(function (values, ind) {
					return {
						id     : ind,
						name   : indicators[ind].short_name,
						values : _.sortBy(values, x)
					};
				})
				.value();

			var stacked = stack(series);

			return stacked;
		}
	},

	methods : {
		draw : function () {
			var svg = d3.select(this.$$.svg);

			var series = svg.select('.data').selectAll('.series')
				.data(this.series, function (d) { return d.id; });

			var x = this.x;

			if (_.isString(x)) {
				x = data.accessor(x);
			}

			var width = Math.floor(this.contentWidth / _(this.datapoints).map(x).uniq().size()) - 1;

			var xScale = d3.time.scale()
				.domain(d3.extent(this.datapoints, x))
				.range([0, this.contentWidth - width]);

			var yScale = d3.scale.linear()
				.domain([0, _(this.series)
					.pluck('values')
					.flatten()
					.map(function (d) {
						return d.y + d.y0;
					})
					.max()])
				.range([this.contentHeight, 0]);

			var color = d3.scale.ordinal().range(palette);

			series.enter()
				.append('g')
				.attr('class', 'series');

			series
				.style('fill', function (d) { return color(d.name); })
				.call(column()
					.values(function (series) { return series.values; })
					.height(function (d) { return yScale(d.y0) - yScale(d.y0 + d.y); })
					.width(width)
					.x(function (d) { return xScale(x(d)); })
					.y(function (d) { return yScale(d.y0 + d.y); })
				);

			series.exit().remove();

			var fmt = d3.format(this.formatString);

			var labels = _(this.series)
				.map(function (s) {
					return _.assign({ name : s.name },
						_.max(s.values, function (d) { return d.campaign.start_date; }));
				})
				.map(function (d) {
					return {
						text    : d.name + ' ' + fmt(d.value),
						x       : xScale(x(d)),
						y       : yScale(d.y0 + d.y),
						defined : data.defined(d.value)
					};
				})
				.reverse()
				.value();

			svg.selectAll('.series.label')
				.data(labels)
				.call(label()
					.addClass('series')
					.width(this.contentWidth)
					.height(this.contentHeight)
					.align(false));

			var t = svg.transition().duration(500);

			t.select('.x.axis')
				.call(d3.svg.axis()
					.orient('bottom')
					.tickSize(0)
					.tickPadding(4)
					.ticks(3)
					.scale(xScale));

			t.select('.y.axis')
				.call(d3.svg.axis()
					.orient('right')
					.tickFormat(fmt)
					.tickSize(this.contentWidth)
					.ticks(3)
					.scale(yScale));

			svg.selectAll('.y.axis text')
				.attr({
					'dx' : -this.contentWidth,
					'dy' : -4
				});
		}
	},

	watch : {
		'datapoints' : 'draw',
		'height'     : 'draw',
		'width'      : 'draw',
	}
};
