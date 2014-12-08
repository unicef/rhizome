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
			loading: false,
			regions: [],
			indicators: [],
			pagination: {
				the_limit: 20,
				the_offset: 0
			},
			table: {
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

	methods: {
		refresh: function () {
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

			this.loading = true;
			this.table.columns = columns;
			this.table.rows = [];

			api.datapoints(options).done(function (data) {
				if (!data.objects || data.objects.length < 1) {
					return;
				}

				var campaigns  = [];
				var datapoints = data.objects.map(function (v) {
					var d = _.pick(v, 'region', 'campaign');

					campaigns.push(d.campaign);

					v.indicators.forEach(function (ind) {
						d[ind.indicator] = ind.value;
					});

					return d;
				});

				self.pagination.the_offset = Number(data.meta.query_dict.the_offset[0]);

				// FIXME: Need to fetch campaign data for displaying proper campaign
				// names instead of IDs in the table.
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
