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
          api.indicators({ id: self.data.indicatorId }, null, { 'cache-control': 'no-cache' })
        ])
        .then(_.spread(function(indicators) {

          var ind = indicators.objects[0]
          // find current indicator
          // var g = _.find(groups.objects, function(d) { return d.id === self.data.groupId });
          self.data.indicatorObject = ind;

          // select current permissions
          // _.each(groupPermissions.objects, function(d) {
          //   if (d.indicator_id) {
          //     self.data.indicatorsSelected.push(self._indicatorIndex[d.indicator_id]);
          //   }
          // });

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
