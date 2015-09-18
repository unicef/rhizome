'use strict';

var Reflux = require('reflux');
var api = require('data/api');

var locationStore = Reflux.createStore({
  init() {
    this.locations = []
    this.locationTypes = []

    this.locationsPromise = api.locations()
      .then(data => {
        this.locations = data.objects;
        this.trigger({
          locations: this.locations
        });
        return this.locations;
      });

    this.locationTypesPromise = api.location_type()
    	.then(data => {
        this.locationTypes = data.objects;
        this.trigger({
          locationTypes: this.locationTypes
        });
        return this.locationTypes;
      });
  },

  getInitialState() {
    return {
      locations: this.locations,
      locationTypes: this.locationTypes,
    };
  },

  // API
  getlocationsPromise() {
    return this.locationsPromise;
  },

  getlocationTypesPromise() {
    return this.locationTypesPromise;
  }
});

module.exports = locationStore;
