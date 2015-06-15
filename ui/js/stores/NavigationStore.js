'use strict';

var _      = require('lodash');
var moment = require('moment');
var Reflux = require('reflux/src');

var api = require('data/api');

var NavigationStore = Reflux.createStore({
	init : function () {
		this.dashboards = [];
		this.customDashboards = [];

		var campaigns = api.campaign()
			.then(function (data) {
				_.each(data.objects, function (campaign) {
					campaign.start_date = moment(campaign.start_date, 'YYYY-MM-DD');
				});

				return data;
			});
		var regions = api.regions({
			read_write  : 'r',
			depth_level : 0
		});
		var dashboards = api.dashboards();

		var customDashboards = api.dashboardsCustom();

		Promise.all([campaigns, regions, dashboards, customDashboards])
			.then(_.spread(this.loadDashboards));
	},

	getInitialState : function () {
		return {
			dashboards : this.dashboards
		};
	},

	loadDashboards : function (campaigns, regions, dashboards, customDashboards) {
		regions   = _(regions.objects);
		campaigns = _(campaigns.objects);

		this.dashboards = _(dashboards.objects)
			.map(function (d) {
				var availableRegions = regions;

				// Filter regions by default office, if one is specified
				if (_.isFinite(d.default_office)) {
					availableRegions = availableRegions.filter(function (r) { return r.office_id == d.default_office; });
				}

				// If no regions for the default office are available, or no default
				// office is provided and this dashboard is limited by office, filter the
				// list of regions to those offices
				if ((!_.isFinite(d.default_office) || availableRegions.size() < 1) && !_.isEmpty(d.offices)) {
					availableRegions = availableRegions.filter(function (r) { return _.includes(d.offices, r.office_id); });
				}

				// If after all of that, there are no regions left that this user is
				// allowed to see for this dashboard, return null so it can be filtered
				if (availableRegions.size() < 1) {
					return null;
				}

				// Take the first region alphabetically at the highest geographic level
				// available as the default region for this dashboard
				var region = availableRegions.sortBy('name').min(_.property('lvl'));

				// Find the latest campaign for the chosen region
				var campaign = campaigns
					.filter(function (c) { return region.office_id === c.office_id; })
					.max(_.method('start_date.valueOf'));

				// Build the path for the dashboard
				var path = region.name + '/' + campaign.start_date.format('YYYY/MM');

				if (!_.endsWith(d.url, '/')) {
					path = '/' + path;
				}

				return _.assign({}, d, { url : d.url + path });
			})
			.reject(_.isNull)
			.value();

		this.customDashboards = _(customDashboards.objects)
			.map(function(d) {
				return {};
			});

		this.trigger({ dashboards : this.dashboards });
	}

});

module.exports = NavigationStore;
