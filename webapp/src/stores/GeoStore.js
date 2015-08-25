'use strict';

var Reflux = require('reflux');
var _ = require('lodash')

var api = require('data/api');

var GeoStore = Reflux.createStore({

  listenables : [require('actions/GeoActions')],

  init : function () {
    this.region = null;
    this.features = [];
  },

  onFetch : function (region) {
    this.region = region;
    Promise.all([
        api.geo({ parent_region__in : region.id }),
        api.geo({ region__in : region.id })
      ])
      .then(this.loadGeography);
  },

  loadGeography : function (responses) {
    this.features = _(responses).pluck('objects.features').flatten().value();
    var border = _.find(this.features, f => f.properties.region_id === this.region.id);

    border.properties.isBorder = true;

    this.trigger({
      reatures : this.reatures
    });
  }
});

module.exports = GeoStore;
