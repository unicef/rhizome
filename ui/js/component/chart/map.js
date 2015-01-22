'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var api    = require('../../data/api');

module.exports = {

	replace: true,
	template: require('./map.html'),

	paramAttributes: [
		'data-indicator',
		'data-range'
	],

	mixins: [
		require('./resize')
	],

	data: function () {
		return {
			error    : false,
			loading  : false,
			region   : null,
			indicator: null,
			date     : null,
			geo      : null,
			border   : null,
			range    : [0, 1]
		};
	},

	ready: function () {
		if (typeof this.range === 'string') {
			this.range = JSON.parse(this.range);
		}
	},

	computed: {

		mappedRegions: function () {
			if (!this.region) {
				return null;
			}

			return _(this.geo.features).flatten('properties').pluck('region_id');
		},

		features: function () {
			return (this.geo && this.geo.features) || [];
		},

		boundingBox: function () {
			function lat(d) {
				return d[1];
			}

			function lng(d) {
				return d[0];
			}

			if (this.features.length < 1) {
				return [[0,0], [0,0]];
			}

			var coordinates = _(this.features).map(function (f) {
				return _.flatten(f.geometry.coordinates, true);
			})
				.flatten(true)
				.value();

			var left   = d3.min(coordinates, lng);
			var right  = d3.max(coordinates, lng);
			var bottom = d3.min(coordinates, lat);
			var top    = d3.max(coordinates, lat);

			return [[left, top], [right, bottom]];
		},

		center: function () {
			var w = this.width || 0;
			var h = this.height || 0;

			return [w/2, h/2];
		},
	},

	methods: {

		draw: function () {
			console.info('map::draw');

			var self = this;

			var svg  = d3.select(this.$el).select('.geography');

			var bounds     = this.boundingBox;
			var projection = d3.geo.albers()
				.parallels([bounds[0][1], bounds[1][1]])
				.scale(1)
				.translate([0, 0]);

			var geopath  = d3.geo.path().projection(projection);
			var features = this.features;
			var width    = this.width || 0;
			var height   = this.height || 0;

			var b = [projection(bounds[0]), projection(bounds[1])];
			var s = 1 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);
			var t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

			projection.scale(s).translate(t);

			var path = svg.selectAll('.region')
				.data(features, function (d) { return d.properties.region_id; });

			path.enter().append('path')
				.on('click', function (d) {
					console.debug('map::click', d.properties.region_id);
					self.region = d.properties.region_id;
				});

			var indicator = this.indicator;
			var quantize  = d3.scale.quantize()
				.domain(this.range)
				.range([1, 2, 3, 4, 5, 6]);

			path.attr({
				'd': geopath,
				'class': function (d) {
					if (!d.properties[indicator]) {
						return 'region';
					}

					return 'region q-' + quantize(d.properties[indicator]);
				}
			});

			path.exit().remove();
		},

		loadData: function () {
			console.info('map::loadData');
			console.debug('map::loadData', 'date', this.date, 'indicator', this.indicator);

			this.loading = true;

			if (!this.date || !this.geo || !this.indicator) {
				return;
			}

			var self = this;

			api.datapoints({
				// campaign_end : moment(this.date).format('YYYY-MM-DD'),
				indicator__in: [this.indicator],
				region__in   : this.mappedRegions,
			}).done(function (data) {
				console.info('map::loadData data received');

				var index    = _.indexBy(data.objects, 'region');
				var features = self.geo.features;

				for (var i = features.length - 1; i >= 0; i--) {
					var f = features[i].properties;
					var d = index[f.region_id];
					var indicators = (d && d.indicators) || [];

					for (var j = indicators.length - 1; j >= 0; j--) {
						var indicator = indicators[j];
						f[indicator.indicator] = indicator.value;
					}
				}

				self.draw();

				self.loading = false;
			}, this.onError);
		},

		loadFeatures: function () {
			console.info('map::loadFeatures');
			console.debug('map::loadFeatures', 'region', this.region);

			if (!this.region) {
				return;
			}

			var self = this;

			this.loading = true;

			Promise.all([api.geo({
				parent_region__in: [this.region]
			}), api.geo({
				region__in: [this.region]
			})]).then(function (data) {
				console.info('map::loadFeatures', 'data received');
				self.geo    = data[0].objects;
				self.border = data[1].objects.features[0];
				console.debug('map::loadFeatures', 'border', self.border);
				self.draw();
			}, this.onError);

		},

		onError: function (err) {
			console.error('map::onError', err);

			this.loading = false;
			this.error = true;
		}

	},

	watch: {
		'region'            : 'loadFeatures',

		'date'              : 'loadData',
		'geo'               : 'loadData',
		'indicator'         : 'loadData',

		'invalidate-display': 'draw',
		'width'             : 'draw',
		'height'            : 'draw'
	}
};
