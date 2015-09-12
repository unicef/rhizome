'use strict';

var Reflux = require('reflux');
var api = require('data/api');

var RegionStore = Reflux.createStore({
  init() {
    this.regions = api.regions()
      .then(data => {
        return data.objects;
      });

    this.regionTypes = api.region_type()
    	.then(data => {
        return data.objects;
      });
  },

  // API
  getRegions() {
    return this.regions;
  },

  getRegionTypes() {
    return this.regionTypes;
  }
});

module.exports = RegionStore;
