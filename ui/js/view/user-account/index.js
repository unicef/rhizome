'use strict';
var Vue  = require('vue');
var _ = require('lodash');
var api = require('../../data/api');
var treeify = require('../../data/transform/treeify');
var ancestoryString = require('../../data/transform/ancestryString');
var MenuVue = require('../../component/menu');

module.exports = {
	template: require('./template.html'),
	data: function(){
	  return {
		roles:[{id:1,title:'Security'},{id:1,title:'Supply'},{id:1,title:'Finance'}],
		regions:[],
		groups:[]    
	  };
	},
	created: function() {
	  var self = this;
	 // console.log(self);
	  self.$set('regionalAccessLoading',true);
	  var MenuComponent = Vue.extend(MenuVue);
	  
	  api.groups().then(function(response){
	     var groups = response.objects;//
	     api.user_groups({'user':self.$parent.$data.user_id}).then(function(data){
	         _.forEach(groups,function(group){
	            
	           group.active = _.some(data.objects,{'group_id':group.id});
	            
	         });
	         self.$set('groups',response.objects); 
	     });
	  });

	  
	  api.regions().then(function(items){
	     self.loadRegionalAccess(); 
	     self.region_map = _.indexBy(items.objects, 'id');
	     var regions = _(items.objects)
	     	.map(function (region) {
	     		return {
	     			'title'  : region.name,
	     			'value'  : region.id,
	     			'id'     : region.id,
	     			'parent' : region.parent_region_id
	     		};
	     	})
	     	.sortBy('title')
	     	.reverse() // I do not know why this works, but it does
	     	.thru(_.curryRight(treeify)('id'))
	     	.thru(ancestoryString)
	     	.value();
	     self.$set('regions',regions);
	     
	  }).then(function () { 
	    self.regionMenu = new MenuComponent({
	    	   el     : '#regions'
	    });
	    self.regionMenu.items = self.$data.regions;
	    self.regionMenu.$on('field-selected',self.addRegionalAccess);
	  }); 
	},
	methods: {
	  addUserGroup: function(groupId){
	     api.map_user_group({'user_id':this.$parent.$data.user_id,'group_id':groupId})
	  },
	  addRegionalAccess: function(data){
	    var self = this;
	    self.$set('regionalAccessLoading',true);
	    api.set_region_permission( {user_id:this.$parent.$data.user_id, region_id:data, read_write:'r' }).then(function(){
	      self.loadRegionalAccess();
	    });
	  },
	  loadRegionalAccess: function(){
	    var self = this;
	    
	    
	    api.region_permission( {user_id:this.$parent.$data.user_id}).then(function(data){
	      var regions = data.objects;
	       _.forEach(regions,function(region){
	           region.name = self.region_map[region.region_id].name;
	       });
	      self.$set('region_permissions',regions); 
	      self.$set('regionalAccessLoading',false);
	    });
	  }
	}
};