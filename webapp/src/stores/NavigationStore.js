'use strict';

var _      = require('lodash');
var moment = require('moment');
var Reflux = require('reflux');

var api = require('data/api');

var builtins = require('dashboard/builtin');

var NavigationStore = Reflux.createStore({
	init : function () {

    this.campaigns        = [];
		this.dashboards       = [];
    this.customDashboards = null;
    this.documents          = [];
    this.loaded           = false;

		var dashboards = api.get_dashboard();
		var documents = api.source_doc();

		var campaigns = api.campaign()
			.then(function (data) {
				_.each(data.objects, function (campaign) {
					campaign.start_date = moment(campaign.start_date, 'YYYY-MM-DD');
				});

				return data;
			});


		var offices = api.office().then(function (response) {
			return _.indexBy(response.objects, 'id');
		});

		Promise.all([campaigns, offices, dashboards, documents])
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

	loadDashboards : function (campaigns, offices, dashboards, documents) {
		var allDashboards = builtins.concat(dashboards.objects);

		campaigns = _(campaigns.objects);

		this.dashboards = _(allDashboards)
			.map(function (d) {
				var availableRegions = [{'id':1, 'name': 'Nigiera', 'parent_region_id': null, 'office_id': 1}];

				console.log('thes are the avail regions')
				console.log(availableRegions)

				// Take the first region alphabetically at the highest geographic level
				// available as the default region for this dashboard
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

		this.documents = _(documents.objects)
			.map(function(d) {
				return d;
			})
			.sortBy('docfile')
			.value();

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

		console.log(' - getting dashboard - ')
		console.log(region_id)

		var dashboard = _.find(this.dashboards, d => _.kebabCase(d.title) === slug);
		var region_promise = api.regions({parent_region_id: 999})

		var regions = _(region_promise.objects).map(function(d) {
				return d;
			}).value();

		console.log(regions)
		// dashboard.region = _.find(regions, d => d.id === region_id);
		// dashboard.regions = regions

		dashboard.regions = [{
				'id': 1,
				'name': 'Nigeriaaaa ',
				'office_id': 1,
				'parent_region_id': null
		},{
				'id': 2,
				'name': 'Paistan! ',
				'office_id': 1,
				'parent_region_id': null
		}]


		return dashboard
  }
});

module.exports = NavigationStore;
