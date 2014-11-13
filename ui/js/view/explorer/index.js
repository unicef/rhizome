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
		var self = this;

		api.indicators().done(function (data) {
			self.$indicators = _.indexBy(data, 'id');
			self.$data.indicators = data.objects.map(function (v) {
				return { selected: false, value: v.id, title: v.name };
			});
		});

		api.regions().done(function (data) {
			self.$regions = _.indexBy(data, 'id');
			self.$data.regions = data.objects.map(function (v) {
				return { selected: false, value: v.id, title: v.name };
			});
		});

		this.$on('page-changed', function (data) {
			this.refresh(data);
		});
	},
	computed: {
		download: function () {
			return api.datapoints.toString({
				indicators: selectedValues(this.indicators),
				regions: selectedValues(this.regions),
				limit: 0,
				format: 'csv'
			});
		}
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
		}
	}
};
