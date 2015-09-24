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
        ])
        .then(_.spread(function(indicators) {

          self.data.indicatorObject = indicators.objects[0];

          self.data.loading = false;
          self.trigger(self.data);
        }));

    }
    // creating new indicator
    else {
      self.data.loading = false;
      self.trigger(self.data);
      }
    },

  // onGetTagTree: function(data){
  //     api.tagTree().then(function(response){
  //       console.log('taG response respone')
  //       return response.objects
  //     }) //
  // },

  onAddIndicatorCalc: function(data){
      console.log('onAddIndicatorCalc ( from the simpleform store )')
      // var self = this;
      // api.set_indicator_to_tag( {indicator_id:this.$parent.$data.indicator_id, indicator_tag_id:data }).then(function(){
      //   self.loadIndicatorTag();
      // });
  },

  onAddTagToIndicator: function(indicator_id, tag_id){
    console.log('addTagToIndicator', indicator_id)
    console.log('for tag: ', tag_id)
    api.set_indicator_to_tag( {indicator_id:indicator_id, indicator_tag_id:tag_id }).then(function(response){
        console.log(response)
    });
  },
  deleteTagFromIndicator: function(data){
    console.log(deleteTagFromIndicator)
    // var self = this;
    // api.set_indicator_to_tag( {indicator_id:this.$parent.$data.indicator_id, indicator_tag_id:data,id:'' }).then(function(){
    //   self.loadIndicatorTag();
    // });
  },

  onInitIndicatorToTag: function(indicator_id) {
    var self = this;

    Promise.all(
      [api.indicator_to_tag({ indicator_id: indicator_id }),
       api.tagTree({},null,{'cache-control':'no-cache'})] // cache_control
      )
      .then(_.spread(function(indicator_to_tag,tag_tree) {
        var allTags = tag_tree.objects
        var indicatorTags = _.map(indicator_to_tag.objects, function(row) {
            return {'id': row.id, 'display': row.indicator_tag__tag_name}
        });

        self.data.rowData = indicatorTags;
        self.data.dropDownData = allTags;

        self.data.loading = false;
        self.trigger(self.data);

        return indicatorTags

      }));
    },

});

module.exports = SimpleFormStore;
