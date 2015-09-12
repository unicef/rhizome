'use strict';

var Reflux = require('reflux');
var api = require('data/api');

var RegionStore = Reflux.createStore({
  init() {
    this.regions = []
    this.regionTypes = []

    this.regionsPromise = api.regions()
      .then(data => {
        this.regions = data.objects;
        this.trigger({
          regions: this.regions
        });
        return this.regions;
      });

    this.regionTypesPromise = api.region_type()
    	.then(data => {
        this.regionTypes = data.objects;
        this.trigger({
          regionTypes: this.regionTypes
        });
        return this.regionTypes;
      });
  },

  getInitialState() {
    return {
      regions: this.regions,
      regionTypes: this.regionTypes,
    };
  },

  // API
  getRegionsPromise() {
    return this.regionsPromise;
  },

  getRegionTypesPromise() {
    return this.regionTypesPromise;
  }
});

module.exports = RegionStore;
