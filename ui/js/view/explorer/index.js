'use strict';

var _        = require('lodash');
var d3       = require('d3');
var moment   = require('moment');

var api      = require('../../data/api');
var Dropdown = require('../../component/dropdown');

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			regions: [],
			indicators: [],
			pagination: {
				limit: 20,
				offset: 0,
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

	attached: function () {
		var self = this;

		this._regions = new Dropdown({
			el     : '#regions',
			source : api.regions,
			mapping: {
				'parent_region_id': 'parent',
				'name'            : 'title',
				'id'              : 'value'
			}
		});

		this._regions.$on('dropdown-value-changed', function (items) {
			self.regions = items;
		});

		this._indicators = new Dropdown({
			el     : '#indicators',
			source : api.indicators,
			mapping: {
				'short_name': 'title',
				'id'        : 'value'
			}
		});

		this._indicators.$on('dropdown-value-changed', function (items) {
			self.indicators = items;
		});

		this.$on('page-changed', function (data) {
			this.refresh(data);
		});
	},

	computed: {

		hasSelection: function () {
			return this.regions.length > 0 && this.indicators.length > 0;
		}

	},

	methods: {

		refresh: function (pagination) {
			if (!this.hasSelection) {
				return;
			}

			var self = this;

			var regionNames = _.indexBy(this.regions, 'value');
			var regions     = _.map(this.regions, 'value');
			var options     = { indicator__in : [] };
			var columns     = [{
					prop: 'region',
					display: 'Region',
					format: function (v) {
						return regionNames[v].title;
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
				options.indicator__in.push(indicator.value);
				columns.push({
					prop   : indicator.value,
					display: indicator.title,
					classes: 'numeric',
					format : function (v) {
						return (isNaN(v) || _.isNull(v)) ? '' : d3.format('n')(v);
					}
				});
			});

			_.defaults(options, pagination, _.omit(this.pagination, 'total_count'));

			this.table.loading = true;
			this.table.columns = columns;
			this.table.rows    = [];

			api.datapoints(options).then(function (data) {
				self.table.loading = false;

				_.assign(self.pagination, _.pick(data.meta, 'limit', 'offset', 'total_count'));

				if (!data.objects || data.objects.length < 1) {
					return;
				}

				var datapoints = data.objects.map(function (v) {
					var d = _.pick(v, 'region');

					d.campaign = moment(v.campaign.start_date).format('MMM YYYY');

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

			var indicators   = _.map(this.indicators, 'value');
			var regions      = _.map(this.regions, 'value');
			var query        = {
				// FIXME: Hack to get around no way of setting no limit for the 12/9 demo.
				'limit'  : 10000000,
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
			if (this.pagination.offset < 1) {
				return;
			}

			this.pagination.offset = Math.max(0, this.pagination.offset - this.pagination.limit);
			this.refresh();
		},

		next: function () {
			this.pagination.offset += this.pagination.limit;
			this.refresh();
		}
	}
};
