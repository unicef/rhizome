'use strict';

var _ = require('lodash');
var api = require('../../data/api');
var Dropdown = require('../../component/dropdown');
var treeify = require('../../data/transform/treeify');

module.exports = {

	template: require('./template.html'),

	data: function () { 
			return {
			    //mapping data from the file import 
			    mappingData: require('./temp_data.js'),
			    //holds the vue master id dropdown components
			    dropdowns:{
			      indicators:[],
			      campaigns:[],
			      regions:[]
			    },
			    //holds arrays of master data for populating the master id dropdowns
			    masterData:{}
			   };
			},
			
	attached: function () {
			var self = this;
			//initialize dropdowns
			_.each(self.$data.mappingData,function(fieldArray,name){
			   	_.each(fieldArray,function(field,key){
			   	   self.$data.dropdowns[name][key] = new Dropdown({
			   	   		el : '#'+name+field.source_id
			   	   	}); 
			   	});
			});
		},
	ready: function() {
	   var self = this;
	   
	   var makeMap = function(data) {
	   	if (data.objects) {
	   		return _.indexBy(data.objects, 'id');
	   	} else {
	   		return null;
	   	}
	   };
	   
	   var connectChildren = function(map, parent_id_key, children_key) {
	   	_.forIn(map, function(d) {
	   		// obj has parent_id?
	   		if (d[parent_id_key] !== undefined && d[parent_id_key] !== null) {
	   			// parent found?
	   			if (map[d[parent_id_key]]) {
	   				var parent = map[d[parent_id_key]];
	   				if (!parent[children_key]) { parent[children_key] = []; }
	   				parent[children_key].push(d);
	   			}
	   		}
	   	});
	   	return map;
	   };
	   
	   //API calls for lists of all regions, indicators, and campaigns
	   Promise.all([
	   	api.regions()
	   		.then(makeMap).then(function(map) {
	   			// create array of children in each parent
	   			return connectChildren(map, 'parent_region_id', 'children');
	   		}),
	    api.indicators()
	        .then(makeMap),
	    api.campaign()
	        .then(makeMap)])
	        .then(function(allData) {
	        
	          self.$data.masterData.regions = allData[0];
	          self.$data.masterData.indicators = allData[1];
	          self.$data.masterData.campaigns = allData[2];
	          self.populateDropdowns();
	        
	        });
	},
	methods: { 
	  populateDropdowns: function(){
	       var self = this;
	        //console.log(self.$data.masterData);
	        _.each(self.$data.masterData,function(data,name){
	             //console.log(data);
	             if(name==='regions')
	             {
        			var items = _.chain(data)
        							.map(function(d) {
        								return {
        									'parent': d.parent_region_id,
        									'title': d.name,
        									'value': d.id
        								};
        							})
        							.value();
	             }
	             else {
	             	var items = _.chain(data)
	             					.map(function(d) {
	             						return {
	             							'parent': null,
	             							'title': d.slug,
	             							'value': d.id
	             						};
	             					})
	             					.value();
	             }

	             
	             // var itemTree = treeify(items, 'value');
	           _.each(self.$data.dropdowns[name],function(dropdown,key){
	                    var mapDataItem = self.$data.mappingData[name][key];
	             	    self.$data.dropdowns[name][key].items = items; 
	             	    self.$data.dropdowns[name][key].itemTree = itemTree; 	

	             	    
	             	    
	             	    if (mapDataItem.mapped)
	             	    {
	             	       self.$data.dropdowns[name][key].select(mapDataItem.master_id);
	             	    }             	   
	             	    
	             	    
	             	    
	             	});
	          
	             
	        });
		} 
	}
};