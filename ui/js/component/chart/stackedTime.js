'use strict';

var _        = require('lodash');
var d3       = require('d3');

var tile     = require('./tile');

var api      = require('../../data/api');
var coolgray = require('../../colors/coolgray');
var format   = require('../../util/format');
var util     = require('../../util/data');

var sort     = require('../../data/transform/sort');

module.exports = {
	replace : true,
	template: require('./stacked.html'),

	paramAttributes: [
		'data-indicators'
	],

	mixins: [
		require('./resize'),
		require('./margin'),
		require('./time-period'),

		require('./hover-line'),
		require('./labels'),

		require('./xAxis'),
		require('./yGrid')
	],

	data: function () {
		return {
			layers    : [],
			indicators: [],
			region    : null,
			date      : null,
			interval  : null,
			loading   : false,
			error     : false,
			x         : d3.scale.linear(),
			y         : d3.scale.linear(),
			xFmt      : format.timeAxis
		};
	},

	compiled: function () {
		// Convert the comma-separated string of indicator ids into an array of
		// numbers. This allows us to take multiple indicators in a single parameter
		// attribute from the template.
		if (typeof this.indicators === 'string') {
			// Assign to the underlying data object to avoid triggering watchers of
			// the indicators property
			this._data.indicators = this.indicators.split(',').map(Number);
		}
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
				return d.values;
			}

			function defined(d) {
				return util.defined(getY(d));
			}

			if (!this.series) {
				this.$set('series', []);
			}

			var self = this;
			var svg  = d3.select(this.$el);

			var stack = d3.layout.stack()
				.x(getX)
				.values(getValues)
				.order('inside-out');

			var layers  = stack(this.layers);

			var dataset = _.flatten(this.layers, 'values');
			var start   = d3.min(dataset, getX) || 0;
			var end     = d3.max(dataset, getX) || start + 1;
			var lower   = Math.min(0, d3.min(dataset, function (d) { return d.y0; }) || 0);
			var upper   = (d3.max(dataset, getY) || lower + 1) * 1.1;

			var x = this.x
				.domain([start, end])
				.range([0, this.contentWidth]);

			var y = this.y
				.domain([lower, upper])
				.range([this.contentHeight, 0]);

			var color = d3.scale.ordinal()
				.domain([0, this.series.length])
				.range(coolgray);

			var area = d3.svg.area()
				.defined(defined)
				.x(function (d) { return x(getX(d)); })
				.y0(function (d) { return y(d.y0); })
				.y1(function (d) { return y(getY(d)); });

			var paths = svg.select('.data').selectAll('.layer')
				.data(layers);

			paths.enter().append('path')
				.attr('class', 'layer');

			paths.attr('d', function (d) {
				return area(getValues(d));
			})
				.style('fill', function (d, i) { return color(i); });

			paths.exit().remove();

			var xs    = _.chain(dataset).pluck('x').sortBy().uniq(true).value();
			var xTile = tile().domain(x.domain());
			var tiles = svg.select('.hover').selectAll('.hover-tile').data(xTile(xs));

			tiles.enter().append('rect')
				.attr('class', 'hover-tile')
				.on({
					'mouseover': function (d) {
						self.$emit('show-annotation', { x: d.value });
					},
					'mouseout': function (d) {
						self.$emit('hide-annotation', { x: d.value });
					}
				});

			tiles.attr({
				'x'     : function (d) { return x(d.lower); },
				'y'     : 0,
				'width' : function (d) { return x(d.upper) - x(d.lower); },
				'height': this.contentHeight
			});

			tiles.exit().remove();

			this._callHook('drawn');
		},

		load: _.throttle(function () {
			// Make sure we have all the required properties to build a query
			if (!this.indicators || !this.region) {
				this.loading = false;
				return;
			}

			this.loading = true;

			var self = this;

			var q = _.extend({
				indicator__in: this.indicators,
				region__in   : [this.region]
			}, this.interval);

			api.datapoints(q)
				.then(function (data) {
					return data.objects;
				})
				.then(sort(function (d) { return d.campaign.start_date; }))
				.then(function (data) {
					var layers = {};

					for (var i = 0, l = data.length; i < l; i++) {
						var d = data[i];
						var values = _.indexBy(d.indicators, 'indicator');

						for (var j = self.indicators.length - 1; j >= 0; j--) {
							var ind = self.indicators[j];

							if (!layers.hasOwnProperty(ind)) {
								layers[ind] = [];
							}

							layers[ind].push({
								x: d.campaign.start_date.getTime(),
								y: values[ind].value
							});
						}
					}

					return _.transform(layers, function (result, values, indicator) {
						result.push({
							'name'  : indicator,
							'values': values
						});
					}, []);
				})
				.done(function (data) {
					self.layers  = data;

					self.$emit('invalidate-display');
				}, this.onError);
		}, 300, { trailing: true, leading: false }),

		onError: function () {
			this.error = true;
		}

	},

	events: {
		'data-load'         : 'load',
		'invalidate-size'   : 'draw',
		'invalidate-display': 'draw'
	}
};
