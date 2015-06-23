'use strict';

var _      = require('lodash');
var moment = require('moment');
var Reflux = require('reflux/src');

var api = require('data/api');

var builtins = require('dashboard/builtin');

var NavigationStore = Reflux.createStore({
	init : function () {
    this.campaigns        = [];
    this.dashboards       = [];
    this.customDashboards = null;
    this.uploads          = [];
    this.loaded           = false;

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

		var dashboards = api.dashboardsCustom();

		var documents = api.document().then(this.loadDocuments);

		var offices = api.office().then(function (response) {
			return _.indexBy(response.objects, 'id');
		});

		this.permissions = [];
		var permissions = api.user_permissions();

		Promise.all([campaigns, regions, offices, permissions, dashboards])
			.then(_.spread(this.loadDashboards));

	},

	getInitialState : function () {
		return {
			campaigns  : this.campaigns,
			dashboards : this.dashboards,
			permissions: this.permissions,
			uploads    : this.documents,
      loaded     : this.loaded
		};
	},

	userHasPermission: function(permissionString) {
		return this.permissions.indexOf(permissionString.toLowerCase()) > -1;
	},

	loadDashboards : function (campaigns, regions, offices, permissions, dashboards) {
		var allDashboards = builtins.concat(dashboards.objects);

		regions   = _(regions.objects);
		campaigns = _(campaigns.objects);

		// parse permissions
		this.permissions = _.map(permissions.objects, function(p) { return p.auth_code; });

		this.dashboards = _(allDashboards)
			.map(function (d) {
				var availableRegions = regions;

				// Filter regions by default office, if one is specified
				if (_.isFinite(d.default_office)) {
					availableRegions = availableRegions.filter(function (r) { return r.office_id == d.default_office; });
				}

				// If no regions for the default office are available, or no default
				// office is provided and this dashboard is limited by office, filter the
				// list of regions to those offices
				if (availableRegions.size() < 1) {
					availableRegions = regions;
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
				var path = '/' + region.name + '/' + campaign.start_date.format('YYYY/MM');

        // Patch the non-comformant API response
        d.charts = d.charts || d.dashboard_json;

				return _.assign({}, d, { href : '/datapoints/' + _.kebabCase(d.title) + path });
			})
			.reject(_.isNull)
			.value();

		this.customDashboards = _(dashboards.objects)
			.map(function(d) {
				return d;
			})
			.sortBy('title')
			.value();

		this.campaigns = campaigns
			.map(function (c) {
				var m          = moment(c.start_date, 'YYYY-MM-DD');
				var dt         = m.format('YYYY/MM');
				var officeName = offices[c.office_id].name;
				var title      = officeName + ': ' + m.format('MMMM YYYY');

				var links = _.map(allDashboards, function (d) {
					return _.defaults({
							path  : _.kebabCase(d.title) + '/' + officeName + '/' + dt
						}, d);
				});

				return _.defaults({
						title      : title,
						dashboards : links
					}, c);
			});

    this.loaded = true;

		this.trigger({
			dashboards : this.dashboards,
			campaigns  : this.campaigns,
      loaded     : this.loaded
		});
	},

	loadDocuments : function (response) {
		var uploads = _.map(response.objects, function (d) {
			var status = (d.is_processed === 'False') ? 'INCOMPLETE' : 'COMPLETE';

			return {
				id     : d.id,
				title  : d.docfile,
				status : status
			};
		});

		this.trigger({
			uploads : uploads
		});
	},

  getDashboard : function (slug) {
    return _.find(this.dashboards, d => _.kebabCase(d.title) === slug);
  }

});

module.exports = NavigationStore;
