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
	  addRemoveUserGroup: function(e){
	     var groupId = e.target.getAttribute('data-group-id');
	     if(e.target.checked)
	     {
	       api.map_user_group({'user_id':this.$parent.$data.user_id,'group_id':groupId});
	     }
	     else {
	       api.map_user_group({'user_id':this.$parent.$data.user_id,'group_id':groupId,id:''})
         }	
  	  },
	  addRegionalAccess: function(data){
	    var self = this;
	    self.$set('regionalAccessLoading',true);
	    api.set_region_permission( {user_id:this.$parent.$data.user_id, region_id:data, read_write:'r' }).then(function(){
	      self.loadRegionalAccess();
	    });
	  },
	  deleteRegionalAccess: function(data){
	    var self = this;
	    api.set_region_permission( {user_id:this.$parent.$data.user_id, region_id:data, read_write:'r',id:'' }).then(function(){
	      self.loadRegionalAccess();
	    });
	  },
	  updateRegionalAccessCanRead: function(e){
	    var self = this;
	    var regionId = e.target.getAttribute('data-region-id');
	    var internalId = e.target.getAttribute('data-internal-id');
	    var readWrite = (e.target.checked?'w':'r');
	    api.set_region_permission( {user_id:this.$parent.$data.user_id, region_id:regionId, read_write:readWrite,id:internalId });
	  },
	  
	  loadRegionalAccess: function(){
	    var self = this;
	    
	    
	    api.region_permission( {user:this.$parent.$data.user_id}).then(function(data){
	      var regions = data.objects;
	       _.forEach(regions,function(region){
	           region.name = self.region_map[region.region_id].name;
	           region.canEnter = region.read_write=='w';
	       });
	      self.$set('region_permissions',regions); 
	      self.$set('regionalAccessLoading',false);
	    });
	  }
	}
};