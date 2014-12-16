'use strict';

var _ = require('lodash');
var api = require('../../data/api');
var d3 = require('d3');

function selectedValues(items) {
	return items.filter(function (o) { return o.selected; })
		.map(function (o) { return o.value; });
}

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			regions: [],
			indicators: [],
			pagination: {
				the_limit: 20,
				the_offset: 0,
				total_count: 0
			},
			table: {
				loading: false,
				columns: ['region', 'campaign'],
				rows: []
			},
			campaign: {
				start: '',
				end: ''
			}
		};
	},

	ready: function () {
		function fetchAll(endPoint, container, cb) {
			return function (data) {
				data.objects.forEach(function (v) {
					container.push({ selected: false, value: v.id, title: v.short_name || v.name });
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

		this.$campaigns = {};

		api.indicators({ limit: 100 }).done(fetchAll(api.indicators, this.indicators, function () {
			self.$broadcast('indicatorsLoaded');
		}));

		api.regions({ limit: 100 }).done(fetchAll(api.regions, this.regions, function () {
			self.$regions = _.indexBy(self.regions, 'value');
			self.$broadcast('regionsLoaded');
		}));

		this.$on('page-changed', function (data) {
			this.refresh(data);
		});
	},

	computed: {
		hasSelection: function () {
			return selectedValues(this.regions).length > 0 &&
				selectedValues(this.indicators).length > 0;
		}
	},

	methods: {
		refresh: function (pagination) {
			if (!this.hasSelection) {
				return;
			}

			var self    = this;

			var regions = selectedValues(this.regions);
			var options = { indicator__in : [] };
			var columns = [{
					prop: 'region',
					display: 'Region',
					format: function (v) {
						return self.$regions[v].title;
					}
				}, {
					prop: 'campaign',
					display: 'Campaign'
				}];

			if (pagination) {
				options.the_limit  = pagination.limit;
				options.the_offset = pagination.offset;
			}

			if (regions.length > 0) {
				options.region__in = regions;
			}

			if (this.campaign.start) {
				options.campaign_start = this.campaign.start;
			}

			if (this.campaign.end) {
				options.campaign_end = this.campaign.end;
			}

			this.indicators.forEach(function (indicator) {
				if (indicator.selected) {
					options.indicator__in.push(indicator.value);
					columns.push({
						prop: indicator.value,
						display: indicator.title,
						classes: 'numeric',
						format: function (v) {
							return (isNaN(v) || _.isNull(v)) ? '' : d3.format('n')(v);
						}
					});
				}
			});

			_.defaults(options, this.pagination);

			this.table.loading = true;
			this.table.columns = columns;
			this.table.rows = [];

			api.datapoints(options).done(function (data) {
				self.table.loading = false;

				self.pagination.the_limit   = Number(data.meta.the_limit);
				self.pagination.the_offset  = Number(data.meta.the_offset);
				self.pagination.total_count = Number(data.meta.total_count);

				if (!data.objects || data.objects.length < 1) {
					return;
				}

				var datapoints = data.objects.map(function (v) {
					var d = _.pick(v, 'region');

					d.campaign = v.campaign.name;

					v.indicators.forEach(function (ind) {
						d[ind.indicator] = ind.value;
					});

					return d;
				});

				self.table.rows = datapoints;
			});
		},

		download: function () {
			if (!this.hasSelection) {
				return;
			}

			this.downloading = true;

			var indicators   = selectedValues(this.indicators);
			var regions      = selectedValues(this.regions);
			var query        = {
				// FIXME: Hack to get around no way of setting no limit for the 12/9 demo.
				'the_limit'  : 10000000,
				'format'     : 'csv',
				'uri_display': 'slug'
			};

			if (indicators.length < 1) {
				this.$data.src = '';
				return;
			}

			query.indicator__in = indicators;
			if (regions.length > 0) {
				query.region__in = regions;
			}

			this.$set('src', api.datapoints.toString(query));
		},

		previous: function () {
			if (this.pagination.the_offset < 1) {
				return;
			}

			this.pagination.the_offset = Math.max(0, this.pagination.the_offset - this.pagination.the_limit);
			this.refresh();
		},

		next: function () {
			this.pagination.the_offset += this.pagination.the_limit;
			this.refresh();
		}
	}
};
