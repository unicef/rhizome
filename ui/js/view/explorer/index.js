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
	methods: {
		refresh: function (pagination) {
			var indicators = selectedValues(this.indicators),
				options = _.defaults({
					indicators: indicators,
					regions: selectedValues(this.regions)
				}, pagination || {}),
				self = this;

			this.table.columns = ['region', 'campaign'].concat(indicators);
			this.table.rows = [];

			api.datapoints(options).done(function (data) {
				self.pagination = data.meta;
				self.table.rows = data.objects;
			});
		}
	}
};
