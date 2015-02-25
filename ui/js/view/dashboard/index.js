'use strict';

var _        = require('lodash');
var moment   = require('moment');
var page     = require('page');

var api      = require('data/api');
var Dropdown = require('component/dropdown');

var titles = {
	'management-dashboard': 'Polio Performance Dashboard',
	'nco-dashboard': 'NGA Country Office'
};

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			campaign  : null,
			campaigns : [],
			dashboard : 'management-dashboard',
			region    : null,
			regionName: '',
			title     : titles['management-dashboard']
		};
	},

	created: function () {
		var show = function (ctx) {
			this.dashboard = ctx.params.dashboard || 'management-dashboard';
			this.title = titles[this.dashboard];
		}.bind(this);

		page('/datapoints/:dashboard', show);
		page({ click: false });

		api.campaign().then(this.loadCampaigns);
	},

	attached: function () {
		var self = this;

		this._regions = new Dropdown({
			el      : '#regions',
			source  : api.regions,
			defaults: 12907, // FIXME: Hard-coded Nigeria default should be supplied by back-end based on permissions
			data: {
				placeholder: 'Loading regions'
			},
			mapping : {
				'parent_region_id': 'parent',
				'name'            : 'title',
				'id'              : 'value'
			}
		});

		this._regions.$on('dropdown-value-changed', function (items) {
			var region = null;
			var name   = '';

			if (items) {
				var pairs = _.pairs(items);

				if (pairs.length > 0) {
					region = pairs[0][0];
					name   = pairs[0][1];
				}
			}

			self.region     = region;
			self.regionName = name;
		});

		this.$.campaigns.$on('dropdown-value-changed', function (items) {
			var campaign = null;
			if (items) {
				var campaigns = _.values(items);

				if (campaigns.length > 0) {
					campaign = campaigns[0];
				}
			}

			self.campaign = campaign;
		});
	},

	methods: {

		loadCampaigns: function (data) {
			this.campaigns = _.uniq(data.objects, function (d) {
				return d.start_date;
				})
				.map(function (o) {
					var startDate = moment(o.start_date, 'YYYY-MM-DD');

					return {
						title   : startDate.format('MMM YYYY'),
						value   : o.start_date,
						date    : startDate.format('YYYYMMDD'),
						end     : o.end_date,
						id      : o.id,
						selected: false
					};
				});

			this.$.campaigns.select(this.campaigns[0].value);
			this.campaign = this.campaigns[0];
		}
	},


	events: {
		'region-changed': function (region) {
			this.region = region;
			this._regions.select(region);
		}
	},

	components: {
		'management-dashboard': require('dashboard/management'),
		'nco-dashboard'       : require('dashboard/nco'),

		'chart-bar'           : require('component/chart/bar'),
		'chart-region-bar'    : require('component/chart/stacked-region-bar'),
		'chart-bullet'        : require('component/chart/bullet'),
		'chart-choropleth'    : require('component/chart/choropleth'),
		'chart-pie'           : require('component/chart/pie'),
		'chart-scatter'       : require('component/chart/scatter'),
		'chart-stacked-area'  : require('component/chart/stacked-area'),
		'chart-line'          : require('component/chart/line'),
		'chart-year-over-year': require('component/chart/year-over-year'),
		'chart-ytd'           : require('component/chart/ytd'),
		'vue-dropdown'        : require('component/dropdown')
	},

	partials: {
		'loading-overlay': require('component/chart/partial/loading-overlay.html')
	}
};
