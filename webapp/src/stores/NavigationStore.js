'use strict';

var _ = require('lodash');
var Reflux = require('reflux');
var moment = require('moment');

var RegionStore = require('stores/RegionStore');
var CampaignStore = require('stores/CampaignStore');

var api = require('data/api');
var builtins = require('dashboard/builtin');

var NavigationStore = Reflux.createStore({
  init: function() {
    this.campaigns = [];
    this.dashboards = [];
    this.customDashboards = null;
    this.documents = [];
    this.loaded = false;

    Promise.all([
    		CampaignStore.getCampaignsPromise(),
    		RegionStore.getlocationsPromise(),
    		api.office().then(response => _.indexBy(response.objects, 'id')),
    		api.get_dashboard(),
    		api.source_doc()
    	])
      .then(_.spread(this._loadDashboards));
  },

  getInitialState: function() {
    return {
      campaigns: this.campaigns,
      dashboards: this.dashboards,
      documents: this.documents,
      loaded: this.loaded
    };
  },

  // API
  getDashboard: function(slug) {
    return _.find(this.dashboards, d => _.kebabCase(d.title) === slug);
  },

  _filterlocations: function(dashboard, locations) {
    if (!_.isFinite(dashboard.default_office)) {
      return locations;
    }

    var availablelocations = locations.filter(function(r) {
      return r.office_id === dashboard.default_office;
    })

    return availablelocations.size() < 1 ? locations : availablelocations;
  },

  // Helpers
  _loadDashboards: function(campaigns, locations, offices, dashboards, documents) {
    var allDashboards = builtins.concat(dashboards.objects);
    var self = this;

    locations = _(locations);
    campaigns = _(campaigns);

    this.dashboards = _(allDashboards)
      .map(function(d) {
        var availablelocations = self._filterlocations(d, locations);

        // If after all of that, there are no locations left that this user is
        // allowed to see for this dashboard, return null so it can be filtered
        if (availablelocations.size() < 1) {
          return null;
        }

        // Take the first location alphabetically at the highest geographic level
        // available as the default location for this dashboard
        var location = availablelocations.sortBy('name').min(_.property('lvl'));

        // Find the latest campaign for the chosen location
        var campaign = campaigns
          .filter(function(c) {
            return location.office_id === c.office_id;
          })
          .max(_.method("moment(start_date, 'YYYY-MM-DD').valueOf"));

        // Build the path for the dashboard
        var path = '';
        try {
          path = '/' + location.name + '/' + moment(campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM');
        } catch (err) {
          path = '/'
        }

        // Patch the non-comformant API response
        d.charts = d.charts || d.dashboard_json;

        return _.assign({}, d, {
          href: '/datapoints/' + _.kebabCase(d.title) + path
        });
      })
      .reject(_.isNull)
      .value();

    this.customDashboards = _(dashboards.objects)
      .sortBy('title')
      .value();

    this.campaigns = campaigns
      .map(c => {
        var m = moment(c.start_date, 'YYYY-MM-DD');
        var dt = m.format('YYYY/MM');
        var officeName = offices[c.office_id].name;
        var title = officeName + ': ' + m.format('MMMM YYYY');

        var links = _.map(allDashboards, function(d) {
          return _.defaults({
            path: _.kebabCase(d.title) + '/' + officeName + '/' + dt
          }, d);
        });

        return _.defaults({
          title: title,
          dashboards: links
        }, c);
      });

    this.documents = _(documents.objects)
      .sortBy('docfile')
      .value();

    this.loaded = true;

    this.trigger({
      dashboards: this.dashboards,
      campaigns: this.campaigns,
      loaded: this.loaded
    });
  }
});

module.exports = NavigationStore;
