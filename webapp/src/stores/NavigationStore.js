'use strict';

var _      = require('lodash');
var moment = require('moment');
var Reflux = require('reflux');

var api = require('data/api');

var builtins = require('dashboard/builtin');
var builtInRegions = require('dashboard/odk/builtInRegion');

var NavigationStore = Reflux.createStore({
	init : function () {

    this.campaigns        = [];
		this.dashboards       = [];
    this.documents          = [];
    this.loaded           = false;

		var campaigns = api.campaign()
			.then(function (data) {
				_.each(data.objects, function (campaign) {
					campaign.start_date = moment(campaign.start_date, 'YYYY-MM-DD');
				});
				return data;
			});

		Promise.all([campaigns])
			.then(_.spread(this.loadDashboards));

	},

	getInitialState : function () {
		return {
			campaigns  : this.campaigns,
			dashboards : this.dashboards,
			documents    : this.documents,
      loaded     : this.loaded
		};
	},

	loadDashboards : function (campaigns) {
		var allDashboards = builtins;

		campaigns = _(campaigns.objects);

		this.dashboards = _(allDashboards)
			.map(function (d) {

				var availableRegions = builtInRegions;
				var region = availableRegions[0]

				// Find the latest campaign for the chosen region
				var campaign = campaigns
					.filter(function (c) { return region.office_id === c.office_id; })
					.max(_.method('start_date.valueOf'));

				// Build the path for the dashboard
				var path = '/' + campaign.start_date.format('YYYY/MM') + '/' + region.id ;

        // Patch the non-comformant API response
        d.charts = d.charts || d.dashboard_json;

				return _.assign({}, d, { href : '/datapoints/' + _.kebabCase(d.title) + path });
			})
			.reject(_.isNull)
			.value();


		this.campaigns = campaigns
			.map(function (c) {
				var m          = moment(c.start_date, 'YYYY-MM-DD');
				var dt         = m.format('YYYY/MM');
				var officeName = c.office_id;
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
		var documents = _.map(response.objects, function (d) {
			var status = (d.is_processed === 'False') ? 'INCOMPLETE' : 'COMPLETE';

			return {
				id     : d.id,
				title  : d.docfile,
				status : status
			};
		});

		this.trigger({
			documents : documents
		});
	},

  getDashboard : function (slug, region_id) {

		var dashboard = _.find(this.dashboards, d => _.kebabCase(d.title) === slug);

		// FIXME: the dashboar regions should be fro the API.. not builtin!!
		// var region_promise = api.regions({parent_region_id: region_id})
		// var regions = _(region_promise.objects).map(function(d) {
		// 		return d;
		// 	}).value();

		dashboard.regions = builtInRegions

		return dashboard
  }
});

module.exports = NavigationStore;
