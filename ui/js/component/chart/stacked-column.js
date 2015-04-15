'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

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
		'data-x',
		'data-x-label'
	],

	mixins : [
		require('./mixin/resize'),
		require('./mixin/margin')
	],

	data : function () {
		return {
			facet        : 'indicator.id',
			formatString : 's',
			series       : [],
			xLabel       : 'MMM [’]YY'
		};
	},

	computed : {
		colWidth : function () {
			return Math.floor(this.contentWidth / d3.max(this.series, function (s) {
				return s.values.length;
			})) - 1;
		},

		empty : function () {
			return !this.series || !this.series.length;
		},

		getX : function () {
			var x = this.x;

			if (_.isString(x)) {
				x = data.accessor(x);
			}

			return x;
		},

		labels : function () {
			var self = this;
			var fmt  = d3.format(this.formatString);

			return _(this.series)
				.map(function (s) {
					return _.assign({ name : s.name },
						_.max(s.values, function (d) { return d.campaign.start_date; }));
				})
				.map(function (d) {
					return {
						text    : d.name + ' ' + fmt(d.value),
						x       : self.xScale(self.getX(d)) + self.colWidth,
						y       : self.yScale(d.y0 + d.y),
						defined : data.defined(d.value)
					};
				})
				.reverse()
				.value();
		},

		xScale : function () {
			var domain = d3.extent(
				_(this.series).pluck('values').flatten().value(),
				this.getX
			);

			return d3.time.scale()
				.domain(domain)
				.range([0, this.contentWidth - this.colWidth]);
		},

		yScale : function () {
			return d3.scale.linear()
				.domain([0, _(this.series)
					.pluck('values')
					.flatten()
					.map(function (d) {
						return d.y + d.y0;
					})
					.max()])
				.range([this.contentHeight, 0]);
		}
	},

	methods : {
		draw : function () {
			var svg = d3.select(this.$$.svg);

			svg.on('mousemove', this.onMouseMove)
				.on('mouseout', this.onMouseOut);

			var x      = this.getX;
			var width  = this.colWidth;
			var xScale = this.xScale;
			var yScale = this.yScale;

			var series = svg.select('.data').selectAll('.series')
				.data(this.series, function (d) { return d.name; });

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

			svg.select('.annotation').selectAll('.series.label')
				.data(this.labels)
				.call(label()
					.addClass('series')
					.width(this.contentWidth)
					.height(this.contentHeight)
					.align(false));

			var t = svg.transition().duration(500);

			var self = this;

			t.select('.x.axis')
				.call(d3.svg.axis()
					.orient('bottom')
					.tickSize(0)
					.tickPadding(4)
					.ticks(4)
					.tickFormat(function (d) {
						return moment(d).format(self.xLabel);
					})
					.scale(xScale));

			svg.selectAll('.x.axis text')
				.attr({
					'text-anchor' : 'middle',
					'dx'          : width / 2
				});

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
		},

		onMouseMove : function () {
			var cursor = d3.mouse(this.$$.svg)[0];
			var x      = this.getX;
			var xScale = this.xScale;
			var yScale = this.yScale;
			var fmt    = d3.format(this.formatString);

			var range = _(this.series)
				.pluck('values')
				.flatten()
				.map(function (d) { return x(d).getTime(); })
				.uniq()
				.sortBy()
				.value();

			var val   = xScale.invert(cursor).getTime();
			var right = d3.bisect(range, val);
			var left  = right - 1;
			var target;

			if (cursor >= 0 || cursor <= this.width) {
				if (left < 0) {
					target = range[right];
				} else if (right >= range.length) {
					target = range[left];
				} else {
					target = val < range[right] ? range[left] : range[right];
				}
			}

			if (target === this._currentHover) {
				return;
			}

			var labels = _(this.series)
				.map(function (s) {
					return _.assign({ name : s.name },
						_(s.values)
							.filter(function (d) {
								return d.campaign.start_date.getTime() === target;
							})
							.first());
				})
				.map(function (d) {
					return {
						text : d.name + ' ' + fmt(d.value),
						x : xScale(x(d)),
						y : yScale(d.y0 + d.y),
						defined: data.defined(d.value)
					};
				})
				.reverse()
				.value();

			var svg = d3.select(this.$$.svg);

			svg.select('.annotation')
				.selectAll('.series.label')
				.data(labels)
				.call(label()
					.addClass('series')
					.width(this.contentWidth)
					.height(this.contentHeight)
					.align(true));

			svg.select('.data')
				.selectAll('rect')
				.transition()
				.duration(300)
				.style('opacity', function (d) {
					return x(d).getTime() === target ? 1 : 0.3;
				});
		},

		onMouseOut : function () {
			var svg = d3.select(this.$$.svg);

			this._currentHover = null;

			svg.select('.annotation')
				.selectAll('.series.label')
				.data(this.labels)
				.call(label()
					.addClass('series')
					.width(this.contentWidth)
					.height(this.contentHeight)
					.align(false));

			svg.select('.data')
				.selectAll('rect')
				.transition()
				.duration(300)
				.style('opacity', 1);
		}
	},

	watch : {
		'series' : 'draw',
		'height' : 'draw',
		'width'  : 'draw',
	}
};
