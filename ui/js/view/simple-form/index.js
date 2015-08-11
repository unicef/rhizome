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
	 // console.log(self);
	  self.$set('tagLoading',true);

		// render tag tree dropdown
		api.tagTree()
			.then(function(response) {
				var ddProps = {
					indicators: response.objects,
					text: 'Add Tag',
					sendValue: self.addTagToIndicator
				};
				self.tagMap = _.indexBy(response.flat, 'id');
				self.indicatorDropdown = React.render(React.createElement(IndicatorTagDropdownMenu, ddProps), document.getElementById("tagSelector"));
			});

	  api.indicator_to_tag({'indicator_id':self.$parent.$data.indicator_id}).then(function(items){
			self.loadIndicatorTag();

	  })
	},
	methods: {
		addTagToIndicator: function(data){
	    var self = this;
	    self.$set('tagLoading',true);
	    api.set_region_permission( {user_id:this.$parent.$data.user_id, region_id:data, read_write:'r' }).then(function(){
	      self.loadRegionalAccess();
	    });
	  },
	  deleteTagFromIndicator: function(data){
	    var self = this;
	    var readWrite = _.find(self.$get('region_permissions'),{region_id:data}).read_write;
	    api.set_region_permission( {user_id:this.$parent.$data.user_id, region_id:data, read_write:readWrite,id:'' }).then(function(){
	      self.loadRegionalAccess();
	    });
	  },
	  loadIndicatorTag: function(){
			// first load the tags, then map the values of the given indicator //
	    var self = this;

			api.indicator_tag().then(function(data){
				var tag_map = data.objects
				self.$set('tag_map',tag_map);
			});

			api.indicator_to_tag({indicator_id:this.$parent.$data.indicator_id}).then(function(data){
				var indicator_tags = data.objects;
				_.forEach(indicator_tags,function(indicator_tag){
				   indicator_tag.tag_name = self.tag_map[indicator_tag.indicator_tag_id].tag_name;
				 });
				self.$set('indicator_tags',indicator_tags);
				self.$set('tagLoading',false);
			});
		},
	}
};
