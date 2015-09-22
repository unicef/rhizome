'use strict';

var Reflux = require('reflux');
var api = require('data/api');

var SimpleFormStore = Reflux.createStore({

  init() {
    console.log('INIT SIMPLE FORM STORE')
    this.indicator = [];

    this.currentIndicatorPromise = api.indicators()
      .then(response => {
        this.indicator = response.objects[0];
        // this.trigger({
        //   locations: this.locations
        // });
        console.log(this.indicator)
        return this.indicator;
      });
  },

  getInitialState() {
    return {
      currentIndicator: this.indicator,
    };
  },

  // API
  getCurrentIndicatorPromise(indicator_id) {
    return this.currentIndicatorPromise.bind(indicator_id);
  },

  // getLocationTypesPromise() {
  //   return this.LocationTypesPromise;
  // }
});

module.exports = SimpleFormStore;
