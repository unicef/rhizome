'use strict';

var Reflux = require('reflux');
var api = require('data/api');
var _      = require('lodash');


var SimpleFormActions = require('actions/SimpleFormActions');


var SimpleFormStore = Reflux.createStore({
  data: {
    indicatorId: null,
    indicatorObject: null,
    loading: true,
    saving: false
  },

  listenables: [ SimpleFormActions ],

  getInitialState: function(){
    return this.data;
  },

  onInitialize: function(indicator_id) {
    var self = this;
    self.data.indicatorId = indicator_id;

    // updating existing group? need to get more data
    if (self.data.indicatorId) {
      Promise.all([
          api.indicators({ id: self.data.indicatorId }, null, { 'cache-control': 'no-cache' }),
          api.indicator_tag()
        ])
        .then(_.spread(function(indicators, indicator_tags) {
          var ind_tags = indicator_tags.objects
          var ind = indicators.objects[0]

          self.data.indicatorObject = ind;
          self.data.indTags = ind_tags;
          self.data.loading = false;
          self.trigger(self.data);
        }));

    }
    // creating new indicator
    else {
      self.data.loading = false;
      self.trigger(self.data);
    }
  }



});

module.exports = SimpleFormStore;
