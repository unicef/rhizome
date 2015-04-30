'use strict';

var _ = require('lodash');
var api = require('../../data/api');
var treeify = require('../../data/transform/treeify');

module.exports = {
	template: require('./template.html'),
	data: function () { 
			return {
			    //mapping data from the file import 
			    mappingData: require('./temp_data.js'),
			    //holds arrays of master data for populating the master id dropdowns
			    remainingVerifications:{
			      indicators:0,
			      campaigns:0,
			      regions:0
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
	   api.document_review({ document_id: Polio.document_id }).then(function(values){
	    console.log(values)
	   }); 
	   
	   var self = this;

	   
	   var regionsPromise = api.regions().then(function(items){
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
	     	.value();
	    
	     self.$set('items.regions',regions); 
	     
	   });
	   var indicatorsPromise = api.indicators()
	       .then(function(items){
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
	   var campaignsPromise = api.campaign().then(function(items){
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
           
	    Promise.all([regionsPromise, indicatorsPromise,campaignsPromise]).then(function () { 
	      self.$set('dataLoaded',true);
	      self.calculateRemainingVerifications();
	    });    
	},
	methods: { 
	  calculateRemainingVerifications:function(){
	    var self = this;
	    _.each(this.mappingData,function(mappingSet,name){ 
	      self.$data.remainingVerifications[name]=0;
	      _.each(mappingSet,function(field){
	            //console.log(field.master_object_id==-1);
	            if(field.master_object_id==-1)
	            {
	               self.$data.remainingVerifications[name]++;
	            }
	       });
	     }); 
	  },
	  populateDropdowns: function(){
	       var self = this;
	        //set up master mapping data from api to be fed into the drop down selects

	        self.calculateRemainingVerifications();
		 
		}
	},
	filters: {
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
	     if(masterIdArray[0]==-1)
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
	     	    console.log(masterIdArray[0]);
	     		return 'master id not set';
	     	}
	     }

	  }
	}
};