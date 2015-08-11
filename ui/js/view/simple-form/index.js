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
			 	self.tag_map = _.indexBy(items.objects, 'id');
			 	var tags = _(items.objects)
				.map(function (tag) {
					return {
						'title'  : tag.tag_name,
						'value'  : region.id,
						'id'     : region.id,
					};
				})
	     	.sortBy('title')
	     	.reverse() // I do not know why this works, but it does
	     	.thru(_.curryRight(treeify)('id'))
	     	.thru(ancestoryString)
	     	.value();
	     self.$set('indicator_tags',ind_tags);

	  }).then(function () {
	    self.tagMenu = new MenuComponent({
	    	   el     : '#indicator_tags'
	    });
	    self.tagMenu.items = self.$data.regions;
	    self.tagMenu.$on('field-selected',self.addRegionalAccess);
	  });
	},
	methods: {
		addTagToIndicator: function(data){
	    var self = this;
	    self.$set('regionalAccessLoading',true);
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
	    var self = this;
			  api.indicator_tag().then(function(data){
	      // var tags = data.objects;
	      //  _.forEach(tags,function(tag){
	      //      tag.tag_name = self.tag_map[tag.indicator_id].tag_name;
	      //  });
	      self.$set('indicator_tags',data.objects);
	      self.$set('tagLoading',false);
	    });
	  }
	}
};
