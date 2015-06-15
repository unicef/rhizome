'use strict';

var _      = require('lodash');
var moment = require('moment');
var Reflux = require('reflux/src');

var api = require('data/api');

var NavigationStore = Reflux.createStore({
	init : function () {
		console.log('NavigationStore::init');

		this.campaigns  = [];
		this.dashboards = [];
		this.uploads    = [];

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

		var documents = api.document().then(this.loadDocuments);

		var offices = api.office().then(function (response) {
			return _.indexBy(response.objects, 'id');
		});

		Promise.all([campaigns, regions, offices, dashboards])
			.then(_.spread(this.loadDashboards));
	},

	getInitialState : function () {
		return {
			campaigns  : this.campaigns,
			dashboards : this.dashboards,
			uploads    : this.documents
		};
	},

	loadDashboards : function (campaigns, regions, offices, dashboards) {
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

				return _.assign({}, d, { href : '/datapoints/' + _.kebabCase(d.title) + path });
			})
			.reject(_.isNull)
			.value();

		this.campaigns = campaigns
			.map(function (c) {
				var m          = moment(c.start_date, 'YYYY-MM-DD');
				var dt         = m.format('YYYY/MM');
				var officeName = offices[c.office_id].name;
				var title      = officeName + ': ' + m.format('MMMM YYYY');

				var links = _.map(dashboards.objects, function (d) {
					return _.defaults({
							path  : _.kebabCase(d.title) + '/' + officeName + '/' + dt
						}, d);
				});

				return _.defaults({
						title      : title,
						dashboards : links
					}, c);
			})

		this.trigger({
			dashboards : this.dashboards,
			campaigns  : this.campaigns,
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
	}
});

module.exports = NavigationStore;
