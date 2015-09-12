'use strict';

var _ = require('lodash');
var Reflux = require('reflux');
var moment = require('moment');

var api = require('data/api');

var DataActions = require('actions/DataActions');

function melt(d) {
  var base = _.omit(d, 'indicators');

  return _.map(d.indicators, function(i) {
    return _.assign({
      indicator: i.indicator,
      value: i.value
    }, base);
  });
}

var DataStore = Reflux.createStore({
  listenables: [DataActions],

  init: function() {
    this.loading = false;
    this.data = [];
  },

  getInitialState: function() {
    return {
      loading: this.loading,
      data: this.data
    };
  },

  onClear: function() {
    this.loading = false;
    this.data = [];

    this.trigger({
      loading: false,
      data: []
    });
  },

  onFetch: function(campaign, region, charts) {
    var m = moment(campaign.start_date, 'YYYY-MM-DD');
    var end = campaign.end_date;

    var promises = _.map(charts, function(def) {
      var q = {
        indicator__in: def.indicators,
        campaign_end: end
      };

      // If no timeRange or startOf property is provided, the chart should fetch
      // data for all time.
      if (!_.isNull(_.get(def, 'timeRange', null)) || def.hasOwnProperty('startOf')) {
        q.campaign_start = m.clone()
          .startOf(def.startOf)
          .subtract(def.timeRange)
          .format('YYYY-MM-DD');
      }

      switch (def.regions) {
        case 'subregions':
          q.parent_region__in = region.id;
          break;

        case 'type':
          var parent = _.get(region, 'parent.id');
          if (!_.isUndefined(parent)) {
            q.parent_region__in = parent;
          }

          q.region_type = region.region_type;
          break;
        default:
          q.region__in = region.id;
          break;
      }

      if (def.level) {
        q.level = def.level;
      }

      return api.datapoints(q);
    });

    Promise.all(promises).then(function(responses) {
      this.data = _(responses)
        .pluck('objects')
        .flatten()
        .map(melt)
        .flatten()
        .value();

      this.loading = false;

      this.trigger({
        loading: false,
        data: this.data
      });
    }.bind(this));

    this.loading = true;
    this.data = [];

    this.trigger({
      loading: true,
      data: []
    });
  }

});

module.exports = DataStore;
