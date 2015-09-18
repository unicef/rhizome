'use strict';

var Reflux = require('reflux');
var _ = require('lodash')

var api = require('data/api');

var GeoStore = Reflux.createStore({

  listenables : [require('actions/GeoActions')],

  init : function () {
    this.location = null;
    this.features = [];
  },

  onFetch : function (location) {
    this.location = location;
    Promise.all([
        api.geo({ parent_location__in : location.id }),
        api.geo({ location__in : location.id })
      ])
      .then(this.loadGeography);
  },

  loadGeography : function (responses) {
    this.features = _(responses).pluck('objects.features').flatten().value();
    var border = _.find(this.features, f => f.properties.location_id === this.location.id);

    border.properties.isBorder = true;

    this.trigger({
      reatures : this.reatures
    });
  }
});

module.exports = GeoStore;
