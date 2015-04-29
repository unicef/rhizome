/* global window, Promise */

'use strict';

var _        = require('lodash');
var moment   = require('moment');
var page     = require('page');
var Vue      = require('vue');

var api            = require('data/api');
var DashboardStore = require('stores/DashboardStore');
var treeify        = require('data/transform/treeify');

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			region     : null,
			campaign   : null,
			dashboard  : null,

			regions    : [],
			campaigns  : [],
			dashboards : [],
		};
	},

	created: function () {
		function show(ctx) {
			self.dashboard = DashboardStore.get(ctx.params.dashboard || 'campaign-performance');
			self.region    = self._regionIndex[ctx.params.region];
			self.campaign  = self._campaignIndex[ctx.params.year + ctx.params.month];
		}

		var self = this;

		this._campaignIndex  = {};
		this._regionIndex    = {};

		page('/datapoints/:dashboard/:region/:year/:month', show);

		// FIXME: The dashboard data will eventually be stored on the server and
		// loaded dynamically
		this.dashboards = _.map(DashboardStore.getAll(), function (dashboard) {
			return {
				'title' : dashboard.name,
				'value' : dashboard.slug
			};
		});

		this.dashboard = DashboardStore.get('management-dashboard');

		var regionPromise = api.regions().then(function (data) {
			var regions = _(data.objects);

			self._regionIndex = _.indexBy(data.objects, 'name');

			self.regions = regions
				.map(function (region) {
					return {
						'title'  : region.name,
						'value'  : region.name,
						'id'     : region.id,
						'parent' : region.parent_region_id
					};
				})
				.sortBy('title')
				.reverse() // I do not know why this works, but it does
				.thru(_.curryRight(treeify)('id'))
				.value();

				return data;
		}, function () {
			window.alert('An error occurred loading regions from the server. Please refresh the page.');
			self.regions = [];
		});

		// FIXME: Filter campaigns by region (or maybe office?)
		var campaignPromise = api.campaign().then(function (data) {
			var campaigns = _(data.objects)
				.forEach(function (campaign) {
					campaign.start_date = moment(campaign.start_date, 'YYYY-MM-DD').toDate();
					campaign.end_date   = moment(campaign.end_date, 'YYYY-MM-DD').toDate();
				})
				.uniq(function (campaign) {
					return moment(campaign.start_date).format('YYYYMM');
				})
				.value();

			self._campaignIndex = _.indexBy(campaigns,
				function (campaign) {
					return moment(campaign.start_date).format('YYYYMM');
				});

			self.campaigns = _.map(campaigns,
				function (campaign) {
					var dt = moment(campaign.start_date);
					return {
						'title' : dt.format('MMMM YYYY'),
						'value' : dt.format('YYYYMM')
					};
				});

			return data;
		}, function () {
			window.alert('An error occurred loading campaign data from the server. Please refresh the page.');
			self.campaigns = [];
		});

		Promise.all([regionPromise, campaignPromise]).then(function (data) {
			page({ click: false });

			var dashboard, region, dt;
			if (!self.region) {
				region = _(data[0].objects)
					.filter(function (region) {
						// FIXME: this only works if the user has permissions to see country-
						// level regions
						return region.parent_region_id === null;
					})
					.sortBy('name')
					.first();
			} else {
				region = self.region;
			}

			if (!self.campaign) {
				var campaign = _(data[1].objects)
					.sortBy(function (campaign) {
						return moment(campaign.start_date).format('YYYYMMDD');
					})
					.last();

				dt = moment(campaign.start_date);
			} else {
				dt = moment(self.campaign.start_date);
			}

			if (!self.dashboard) {
				dashboard = 'campaign-performance';
			} else {
				dashboard = self.dashboard.slug;
			}

			if (dashboard && region && dt) {
				page('/datapoints/' + dashboard + '/' + region.name + '/' +
					dt.format('YYYY') + '/' +
					dt.format('MM'));
			}
		});
	},

	methods : {
		navigate : function (dashboard, region, campaign) {
			page('/datapoints/' +
				dashboard.slug + '/' +
				region.name + '/' +
				moment(campaign.start_date).format('YYYY/MM'));
		}
	},

	events: {
		'region-selected' : function (region) {
			this.navigate(
				this.dashboard,
				this._regionIndex[region],
				this.campaign);
		},

		'campaign-selected' : function (campaign) {
			this.navigate(
				this.dashboard,
				this.region,
				this._campaignIndex[campaign]);
		},

		'dashboard-selected' : function (dashboard) {
			var db = DashboardStore.get(dashboard);
			this.navigate(
				db,
				this._regionIndex[db.region] || this.region,
				this.campaign);
		}
	},

	filters : {
		'date' : function (v, format) {
			return moment(v).format(Vue.util.stripQuotes(format));
		}
	},

	components: {
		'management-dashboard'    : require('dashboard/management'),
		'nga-campaign-monitoring' : require('dashboard/nco'),

		'chart-bar'               : require('component/chart/bar'),
		'chart-bullet'            : require('component/chart/bullet'),
		'chart-choropleth'        : require('component/chart/choropleth'),
		'chart-line'              : require('component/chart/line'),
		'chart-pie'               : require('component/chart/pie'),
		'chart-scatter'           : require('component/chart/scatter'),
		'chart-stacked-area'      : require('component/chart/stacked-area'),
		'chart-stacked-bar'       : require('component/chart/stacked-bar'),
		'chart-stacked-column'    : require('component/chart/stacked-column'),
		'chart-year-over-year'    : require('component/chart/year-over-year'),
		'chart-ytd'               : require('component/chart/ytd'),

		'vue-dropdown'            : require('component/dropdown')
	},

	partials: {
		'loading-overlay': require('component/chart/partial/loading-overlay.html')
	}
};
