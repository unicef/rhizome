'use strict';

var _ = require('lodash');
var Reflux = require('reflux');
var moment = require('moment');

var CampaignStore = require('stores/CampaignStore');

var api = require('data/api');
var builtins = require('dashboard/builtin');

var NavigationStore = Reflux.createStore({
  init: function () {
    this.campaigns = [];
    this.dashboards = [];
    this.customDashboards = [];
    this.loaded = false;

    Promise.all([
      CampaignStore.getCampaignsPromise(),
      api.office()
    ]).then(_.spread(this._loadDashboards));
  },

  getInitialState: function () {
    return {
      campaigns: this.campaigns,
      dashboards: this.dashboards,
      documents: this.documents,
      loaded: this.loaded
    };
  },

  // API
  getDashboard: function (slug) {
    var dashboard = _.find(this.dashboards, d => _.kebabCase(d.title) === slug)
    if (dashboard.id <= 0) {
      return new Promise(resolve => {
        resolve(dashboard)
      })
    } else {
      return api.get_chart({dashboard_id: dashboard.id}, null, {'cache-control': 'no-cache'}).then(res => {
        dashboard.charts = res.objects.map(chart => {
          var result = chart.chart_json;
          result.id = chart.id;
          return result;
        });
        return dashboard
      }, function (err) {
        console.log(err);
        dashboard.charts = [];
      });
    }
  },

  // Helpers
  _loadDashboards: function (campaigns, offices) {
    var allDashboards = builtins;

    campaigns = _(campaigns);
    var chainOffices = _(offices.objects);

    this.dashboards = _(allDashboards)
      .map(function (d) {
        // Take the first location alphabetically at the highest geographic level
        // available as the default location for this dashboard
        var location = chainOffices.min(_.property('id'));

        // Find the latest campaign for the chosen location
        var campaign = campaigns
          .filter(c => {
            return location.id === c.office_id;
          })
          .max(c => {
            return moment(c.start_date, 'YYYY-MM-DD').valueOf()
          });


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

    this.campaigns = campaigns
      .map(c => {
        var m = moment(c.start_date, 'YYYY-MM-DD');
        var dt = m.format('YYYY/MM');
        var officeName = _.indexBy(offices.objects, 'id')[c.office_id].name;
        var title = officeName + ': ' + m.format('MMMM YYYY');

        var links = _.map(allDashboards, function (d) {
          return _.defaults({
            path: _.kebabCase(d.title) + '/' + officeName + '/' + dt
          }, d);
        });

        return _.defaults({
          title: title,
          dashboards: links
        }, c);
      });

    this.loaded = true;

    this.trigger({
      dashboards: this.dashboards,
      campaigns: this.campaigns,
      loaded: this.loaded
    });
  }
});

module.exports = NavigationStore;
