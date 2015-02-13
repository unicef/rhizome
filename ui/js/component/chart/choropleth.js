'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');

var api    = require('data/api');

module.exports = {

	replace: true,
	template: require('./choropleth.html'),

	paramAttributes: [
		'data-indicator',
		'data-range'
	],

	mixins: [
		require('./mixin/resize')
	],

	partials: {
		'loading-overlay': require('./partial/loading-overlay.html')
	},

	data: function () {
		return {
			error    : false,
			loading  : false,
			region   : null,
			indicator: null,
			campaign : null,
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

		centroid: function () {
			var box = this.boundingBox;
			var lat = box[1][1] + ((box[0][1] - box[1][1]) / 2);
			var lng = box[0][0] + ((box[1][0] - box[0][0]) / 2);

			return [lng, lat];
		}
	},

	methods: {
		draw: function () {
			var self = this;

			var svg  = d3.select(this.$el).select('.geography');

			var bounds     = this.boundingBox;

			var width    = this.width || 0;
			var height   = this.height || 0;

			var projection = d3.geo.conicEqualArea()
				.parallels([bounds[1][1], bounds[0][1]])
				.rotate([-this.centroid[0], 0])     // Rotate the globe so that the country is centered horizontally
				.center([0, this.centroid[1]])      // Set the center of the projection so that the polygon is moved vertically into the center of the viewport
				.translate([width / 2, height / 2]) // Translate to the center of the viewport
				.scale(1);

			var geopath  = d3.geo.path().projection(projection);
			var features = this.features;

			// Calculate the scale required to fit the map within the SVG view box.
			var b = [projection(bounds[0]), projection(bounds[1])];
			var s = 1 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);

			projection.scale(s);

			var path = svg.selectAll('.region')
				.data(features, function (d) { return d.properties.region_id; });

			path.enter().append('path')
				.on('click', function (d) {
					self.$dispatch('region-changed', d.properties.region_id);
				})
				.on('mousemove', function (d) {
					var evt = d3.event;

					console.debug('choropleth::mousemove', evt.pageX, evt.pageY);

					// Do not show a tooltip if we have no name
					if (!d.properties.name) {
						return;
					}

					self.$dispatch('tooltip-show', {
						el      : this,
						position: {
							x: evt.pageX,
							y: evt.pageY,
						},
						data: {
							text: d.properties.name
						}
					});
				})
				.on('mouseout', function () {
					self.$dispatch('tooltip-hide', { el: this });
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

					return 'region clickable q-' + quantize(d.properties[indicator]);
				}
			});

			path.exit().remove();
		},

		loadData: function () {
			this.loading = true;

			if (!this.campaign || !this.geo || !this.indicator) {
				return;
			}

			var self = this;

			api.datapoints({
				campaign_end  : this.campaign.end,
				campaign_start: this.campaign.end,
				indicator__in : [this.indicator],
				region__in    : this.mappedRegions
			}).done(function (data) {

				var index    = _.indexBy(data.objects, 'region');
				var features = self.features;

				for (var i = features.length - 1; i >= 0; i--) {
					var f          = features[i].properties;
					var d          = index[f.region_id];
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
				self.geo    = data[0].objects;
				self.border = data[1].objects.features[0];

				// FIXME: Can't filter regions by ID, so we have to fetch all of them
				// and just pick out the ones we want.
				api.regions().then(function (data) {
					var regions = _.indexBy(data.objects, 'id');

					self.geo.features.forEach(function (feature) {
						feature.properties.name = regions[feature.properties.region_id].name;
					});
				});

				self.draw();
			}, this.onError);
		},

		onError: function (err) {
			console.err('choropleth', err);
			this.loading = false;
			this.error = true;
		}
	},

	watch: {
		'region'            : 'loadFeatures',

		'campaign'          : 'loadData',
		'geo'               : 'loadData',
		'indicator'         : 'loadData',

		'invalidate-display': 'draw',
		'width'             : 'draw',
		'height'            : 'draw'
	}
};
