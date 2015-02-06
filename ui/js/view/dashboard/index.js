'use strict';

var moment   = require('moment');
var page     = require('page');

var api      = require('data/api');
var Dropdown = require('component/dropdown');

var titles = {
	'management-dashboard': 'Polio Performance Dashboard',
	'nco-dashboard': "NGA Country Office"
};

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			campaign : null,
			campaigns: [],
			dashboard: 'management-dashboard',
			region   : null,
			title    : titles['management-dashboard']
		};
	},

	created: function () {
		var show = function (ctx) {
			console.debug('dashboard::show', ctx.params.dashboard);
			this.dashboard = ctx.params.dashboard || 'management-dashboard';
			this.title = titles[this.dashboard];
		}.bind(this);

		page('/datapoints/:dashboard', show);
		page({ click: false });
	},

	attached: function () {
		var self = this;

		this._regions = new Dropdown({
			el      : '#regions',
			source  : api.regions,
			defaults: 12907, // FIXME: Hard-coded Nigeria default should be supplied by back-end based on permissions
			mapping : {
				'parent_region_id': 'parent',
				'name'            : 'title',
				'id'              : 'value'
			}
		});

		this._regions.$on('dropdown-value-changed', function (items) {
			self.region = (items && items.length > 0) ? items[0].value : null;
		});

		this.$.campaigns.$on('dropdown-value-changed', function (items) {
			self.campaign = (items && items.length > 0) ? items[0] : null;
		});
	},

	methods: {

		loadCampaigns: function (data) {
			this.campaigns = data.objects.map(function (o) {
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

			this.campaigns[0].selected = true;
			this.campaign = this.campaigns[0];
		}
	},

	watch: {

		'region': function () {
			api.campaign({ region__in: this.region }).then(this.loadCampaigns);
			this._regions.$emit('dropdown-select', this.region);
		}

	},

	events: {
		'region-changed': function (region) {
			this.region = region;
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
