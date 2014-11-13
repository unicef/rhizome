'use strict';

var _ = require('lodash');
var api = require('../../data/api');

function selectedValues(items) {
	return items.filter(function (o) { return o.selected; })
		.map(function (o) { return o.value; });
}

module.exports = {
	template: require('./template.html'),
	data: {
		loading: false,
		regions: [],
		indicators: [],
		pagination: {
			limit: 0,
			offset: 0
		},
		table: {
			columns: ['region', 'campaign'],
			rows: []
		}
	},
	ready: function () {
		function fetchAll(endPoint, container, cb) {
			return function (data) {
				data.objects.forEach(function (v) {
					container.push({ selected: false, value: v.id, title: v.name });
				});

				if (data.meta.next) {
					endPoint({
						limit: data.meta.limit,
						offset: data.meta.limit + data.meta.offset
					}).done(fetchAll(endPoint, container, cb));
				} else {
					cb();
				}
			};
		}

		var self = this;

		api.indicators({ limit: 100 }).done(fetchAll(api.indicators, this.indicators, function () {
			self.$broadcast('indicatorsLoaded');
		}));

		api.regions({ limit: 100 }).done(fetchAll(api.regions, this.regions, function () {
			self.$broadcast('regionsLoaded');
		}));

		this.$on('page-changed', function (data) {
			this.refresh(data);
		});
	},
	methods: {
		refresh: function (pagination) {
			var indicators = selectedValues(this.indicators),
				regions = selectedValues(this.regions),
				options = {},
				self = this;

			if (indicators.length > 0) {
				options.indicator__in = indicators;
			}

			if (regions.length > 0) {
				options.region__in = regions;
			}

			_.defaults(options, pagination || { limit : indicators.length * 20 });

			this.loading = true;
			this.table.columns = ['region', 'campaign'].concat(indicators);
			this.table.rows = [];

			api.datapoints(options).done(function (data) {
				// data.objects is an object that maps an indicator name to an array of
				// values that each correspond to one unique combination of (region,
				// campaign). Here we pivot this data so we have an array of objects,
				// one for each unique (region, campaign) combination with each
				// indicator set as a property on the object.
				var datapoints = _(data.objects).transform(function (result, value, key) {
					// Convert the object to an array of objects, melting the properties
					// of the original object into each object as the value of an
					// `indicator` property.
					value.forEach(function (o) {
						o.indicator = key;
						result.push(o);
					});
				}, []).transform(function (result, o) {
					var key = String([o.region, o.campaign]);

					if (!result.hasOwnProperty(key)) {
						result[key] = _.omit(o, 'value', 'indicator');
					}

					result[key][o.indicator] = o.value;
				}, {}).values().sortBy('region').value();

				self.pagination = data.meta;

				self.table.columns = ['region', 'campaign'].concat(_.keys(data.objects));
				self.table.rows = datapoints;

				self.loading = false;
			});
		},
		download: function () {
			this.downloading = true;
			var indicators = selectedValues(this.indicators),
				regions = selectedValues(this.regions),
				query = {
					limit: 0,
					format: 'csv'
				};

			if (indicators.length < 1) {
				this.$data.src = '';
				return;
			}

			query.indicator__in = indicators;
			if (regions.length > 0) {
				query.region__in = regions;
			}

			this.$data.src = api.datapoints.toString(query);
		}
	}
};
