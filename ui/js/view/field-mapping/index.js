'use strict';
var Vue  = require('vue');
var _ = require('lodash');
var api = require('../../data/api');
var treeify = require('../../data/transform/treeify');
var ancestoryString = require('../../data/transform/ancestryString');
var MenuVue = require('../../component/menu');

module.exports = {
	template: require('./template.html'),
	data: function () { 
			return {
			    //mapping data from the file import 
			    mappingData: {},//require('./temp_data.js'),
			    //holds arrays of master data for populating the master id dropdowns
			    remainingVerifications:{
			      indicators:0,
			      campaigns:0,
			      regions:0,
			      total:0
			    },
			    items:{
			      indicators:[],
			      campaigns:[],
			      regions:[]
			    },
			    maps:{}, //holds hashes for indicators, campaigns, and regions
			    dataLoaded:false
			   };
			},
			
	created: function() {
	  var self = this;
	  var regionsPromise, indicatorsPromise, campaignsPromise, documentPromise;
	   documentPromise = api.document_review({ document: this.$parent.$data.document_id }).then(function(values){
	      self.$set('mappingData',values.objects);
	    });
	   regionsPromise = api.regions().then(function(items){
	     self.maps.regions = _.indexBy(items.objects, 'id');
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
	     //console.log(regions);
	     self.$set('items.regions',regions); 
	     
	   });
	   indicatorsPromise = api.indicators().then(function(items){
	           self.maps.indicators = _.indexBy(items.objects, 'id');
	          var indicators = _(items.objects)
	           	.map(function (indicator) {
	           		return {
	           			'title'  : indicator.slug,
	           			'value'  : indicator.id,
	           			'id'     : indicator.id,
	           			'parent' : null
	           		};
	           	})
	           	.sortBy('title')
	           	.reverse() 
	           	.value();
	          
	           self.$set('items.indicators',indicators);
	          
	          
	       });
	   campaignsPromise = api.campaign().then(function(items){
	          self.maps.campaigns = _.indexBy(items.objects, 'id');
	          var campaigns = _(items.objects)
	           	.map(function (campaign) {
	           		return {
	           			'title'  : campaign.slug + '_' + campaign.id,
	           			'value'  : campaign.id,
	           			'id'     : campaign.id,
	           			'parent' : null
	           		};
	           	})
	           	.sortBy('title')
	           	.reverse() 
	           	.value();
	          
	           self.$set('items.campaigns',campaigns);
	           
	       });
           
	    Promise.all([regionsPromise, indicatorsPromise,campaignsPromise,documentPromise]).then(function () { 
	      self.$set('dataLoaded',true);
	      self.calculateRemainingVerifications();
	      self.initializaMenus();
	    });    
	},
	methods: { 
	  displayUnmap: function(element){
	    var type = element.$parent.$key;
	    var field = element.$data.field;
	    var key = _.findIndex(this.$data.mappingData[type],{'source_object_id':field.source_object_id});
	    this.mappingData[type][key].master_object_id = '-1';
	    api.map_field({ 'source_object_id': element.$data.field.source_object_id,
	    				'master_object_id': null,
	    				'object_type'  : type.substr(0, type.length-1) }).then(function(values){
	    				    
	    				   // console.log(values);
	    				    
	    				});
	    this.calculateRemainingVerifications();
	  },
	  calculateRemainingVerifications:function(){
	    var self = this;
	    self.$data.remainingVerifications.total=0;
	    _.each(this.mappingData,function(mappingSet,name){ 
	      self.$data.remainingVerifications[name]=0;
	      _.each(mappingSet,function(field){
	            //console.log(field.master_object_id==-1);
	            if(field.master_object_id===-1)
	            {
	               self.$data.remainingVerifications[name]++;
	               self.$data.remainingVerifications.total++;
	            }
	       });
	     }); 
	  },
	  populateDropdowns: function(){
	       var self = this;
	        //set up master mapping data from api to be fed into the drop down selects

	        self.calculateRemainingVerifications();
		 
	  },
	  processMenuClick: function(value){
	    console.log(this,value);
	  },
	  initializaMenus: function(){
	     var MenuComponent = Vue.extend(MenuVue);
	     var self = this;
	     
	     var setMasterId = function(type, sourceId, masterId)
	     {  
	        var key = _.findIndex(self.$data.mappingData[type],{'source_object_id':sourceId});
	        self.mappingData[type][key].master_object_id = masterId;
	        api.map_field({ 'source_object_id': sourceId,
	        				'master_object_id': masterId,
	        				'object_type'  : type.substr(0, type.length-1) }).then(function(values){
	        				    
	        				    console.log(values);
	        				    
	        				});
	        self.calculateRemainingVerifications();
	     
	     };
	     var setMasterIdCurry = _.curry(setMasterId);
	     
	     self._menus = {
	       regions:{},
	       campaigns:{},
	       indicators:{}
	     };
	     _.each(self.$data.mappingData, function(data,type){
	       _.each(data,function(field){
	            self._menus[type][field.source_object_id] = new MenuComponent({
	           	   el     : '#'+type+field.source_object_id+'menu'
	           });
	           self._menus[type][field.source_object_id].items = self.$data.items[type];
	           self._menus[type][field.source_object_id].$on('field-selected',setMasterIdCurry(type,field.source_object_id));
	       });
	     });
	  }   
	},
	filters: {
	  check: function(masterId){
	    if(masterId !== -1)
	    {
	      return 'fa fa-check fa-3x';
	    }
	    else {
	      return '';
	    }
	  },
	  fixVerificationPluralization: function(field,digit){
		  if(this[digit][field]===1){
		    return field.substring(0, field.length - 1) + ' needs';
		  }
		  else {
		  	return field + ' need';
		  }
	  },
	  buttonDisplay: function(masterIdString){
	    var masterIdArray = masterIdString.split('_');
	     if(masterIdArray[0]==='-1')
	     {
	       return 'click to map';
	     }
	     else {
	     	var val =this.maps[masterIdArray[1]][masterIdArray[0]];
	     	if(masterIdArray[1]==='regions' && val)
	     	{
	     	  return val.name;
	     	}
	     	else if(val)
	     	{
	     	  return val.slug;
	     	}
	     	else {
	     		return 'master id not set';
	     	}
	     }

	  }
	}
};