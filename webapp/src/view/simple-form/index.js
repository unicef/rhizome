'use strict';
var Vue  = require('vue');
var _ = require('lodash');
var api = require('../../data/api');
var treeify = require('../../data/transform/treeify');
var ancestoryString = require('../../data/transform/ancestryString');
var MenuVue = require('../../component/vue-menu');
var React  = require('react');
var IndicatorTagDropdownMenu = require('component/IndicatorTagDropdownMenu.jsx');

module.exports = {
	template: require('./template.html'),
	data: function(){
	  return {
		regions:[],
		groups:[]
	  };
	},
	created: function() {
	  var self = this;

	  self.$set('tagLoading',true);

		// load indicators in the table
		self.loadIndicatorTag();

		// render tag tree dropdown
		api.tagTree() //
			.then(function(response) {
				var ddProps = {
					tag_tree: response.objects,
					text: 'Add Tag',
					sendValue: self.addTagToIndicator
				};
				self.indicatorDropdown = React.render(React.createElement(IndicatorTagDropdownMenu, ddProps), document.getElementById("tagSelector"));
			});

	},
	methods: {
		addTagToIndicator: function(data){
	    var self = this;
	    self.$set('tagLoading',true);
	    api.set_indicator_to_tag( {indicator_id:this.$parent.$data.indicator_id, indicator_tag_id:data }).then(function(){
	      self.loadIndicatorTag();
	    });
	  },
	  deleteTagFromIndicator: function(data){
	    var self = this;
	    api.set_indicator_to_tag( {indicator_id:this.$parent.$data.indicator_id, indicator_tag_id:data
				,id:'' }).then(function(){
	      self.loadIndicatorTag();
	    });
	  },
	  loadIndicatorTag: function(){
			// first load the tags, then map the values of the given indicator //
	    var self = this;
	    self.$set('tagLoading',true);

			api.indicator_tag().then(function(data){
				var tag_map = [];
				var indicator_tags = data.objects;
				_.forEach(indicator_tags,function(tag){
					tag_map[tag.id] = tag.tag_name;
				});
				self.$set('tag_map',tag_map);
			});

			api.indicator_to_tag({indicator_id:this.$parent.$data.indicator_id},null,{'cache-control':'no-cache'}).then(function(data){
				var indicator_tags = data.objects;
				_.forEach(indicator_tags,function(indicator_tag){
				   indicator_tag.tag_name = self.tag_map[indicator_tag.indicator_tag_id];
				 });
				self.$set('indicator_tags',indicator_tags);
				self.$set('tagLoading',false);
			});
		},
	}
};
