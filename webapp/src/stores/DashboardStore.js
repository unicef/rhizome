'use strict';

var _ = require('lodash');
var Reflux = require('reflux');
var moment = require('moment');

var RegionStore = require('stores/RegionStore');
var CampaignStore = require('stores/CampaignStore');

var api = require('data/api');
// var builtins = require('dashboard/builtin');

var DashboardStore = Reflux.createStore({
  listenables: [require('actions/DashboardActions')],

  init: function() {
    this.loaded = false;
    this.indicators = {};
    Promise.all([
        RegionStore.getRegionsPromise(),
        RegionStore.getRegionTypesPromise(),
	    	CampaignStore.getCampaignsPromise(),
    	])
      .then(_.spread((regions, regionsTypes, campaigns)=> {
        this.regions = regions;
        this.campaigns = campaigns;

        var regionIdx = _.indexBy(regions, 'id');
        var types = _.indexBy(regionsTypes, 'id');

        _.each(this.regions, function(r) {
          r.region_type = _.get(types[r.region_type_id], 'name');
          r.parent = regionIdx[r.parent_region_id];
        });

        this.loaded = true;

        this.trigger({
          loaded: this.loaded,
          regions: this.regions,
          campaigns: this.campaign
        });
      }));
  },

  getQueries: function() {
    var indicators = this.indicators;
    var qs = _.groupBy(indicators, function(definition, key) {
      return [
        definition.duration,
        definition.startOf,
        definition.regions
      ].join('-');
    });
    return _.map(qs, function(arr) {
      return _.merge.apply(null, arr.concat(function(a, b) {
        if (_.isArray(a)) {
          return a.concat(b);
        }
      }));
    });
  },

  // action handlers
  onSetDashboard: function(definition) {
    console.log("DashboardStore -> onSetDashboard:", definition)
    var dashboard = this.dashboard = definition.dashboard;
    this.region = definition.region || this.region;
    this.date = definition.date || this.date;

    if (!this.loaded) {
      return;
    }

    this.indicators = {};
    _.each(dashboard.charts, this.addChartDefinition);

    var regions = this.regions;
    var campaigns = this.campaigns;

    var regionIdx = _.indexBy(regions, 'id');
    var topLevelRegions = _(regions)
      .filter(function(r) {
        return !regionIdx.hasOwnProperty(r.parent_region_id);
      })
      .sortBy('name');

    var region = _.find(regions, function(r) {
      return r.name === this.region;
    }.bind(this));
    console.log("2:", this.region, region);

    /**

      Question ???
      - onSetDashboard receives correct region, but after this condition rewrites it to Nigeria

    **/
    if (_.isFinite(dashboard.default_office_id) && _.get(region, 'office_id') !== dashboard.default_office_id) {
      region = topLevelRegions.find(function(r) {
        return r.office_id === dashboard.default_office_id;
      });
    }

    if (!region) {
      region = topLevelRegions.first();
    }
    console.log("4:", this.region, region);

    var campaign = _(campaigns)
      .filter(function(c) {
        return c.office_id === region.office_id &&
          (!this.date || _.startsWith(c.start_date, this.date));
      }.bind(this))
      .sortBy('start_date')
      .last();

    var hasMap = _(dashboard.charts)
      .pluck('type')
      .any(t => _.endsWith(t, 'Map'));


    console.log("AFTER:", region);
    this.trigger({
      dashboard: this.dashboard,
      region: region,
      campaign: campaign,
      loaded: true,

      regions: regions,
      campaigns: _.filter(campaigns, function(c) {
        return c.office_id === region.office_id;
      }),
      hasMap: hasMap,
    });
  },

  onSetRegion: function(id) {
    var region = _.find(this.regions, function(r) {
      return r.id === id;
    }.bind(this));

    if (region) {
      this.trigger({
        region: region
      });
    }
  },

  // helpers
  addChartDefinition: function(chart) {
    var base = _.omit(chart, 'indicators', 'title');

    _.each(chart.indicators, function(id) {
      var duration = !_.isNull(_.get(chart, 'timeRange', null)) ? moment.duration(chart.timeRange) : Infinity;
      var hash = [id, chart.startOf, chart.regions].join('-');

      if (!this.indicators.hasOwnProperty(hash) || duration > this.indicators[hash].duration) {
        this.indicators[hash] = _.defaults({
          duration: duration,
          indicators: [id]
        }, base);
      }
    }.bind(this));
  }
});

module.exports = DashboardStore;
