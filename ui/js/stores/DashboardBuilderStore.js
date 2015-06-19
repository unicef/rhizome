'use strict';

var _      = require('lodash');
var Reflux = require('reflux/src');
var api = require('data/api');

var treeify = require('data/transform/treeify');
var ancestoryString = require('data/transform/ancestryString');
var moment = require('moment');

var DashboardActions  = require('actions/DashboardActions');

var DashboardBuilderStore = Reflux.createStore({
	listenables : [require('actions/DashboardBuilderActions')],
	getInitialState: function(){
	   return this.data;
	},
	data:{charts:[],
	      regions:[],
	      campaigns:[],
	      indicators:{},
	      loaded:false,
	      newDashboard:false,
	      dashboardTitle:'',
	      },
	onInitialize : function(id){
	var self = this;
	 this.data.dashboardId = id;
	 if(_.isNull(id))
	 {
	 	this.data.newDashboard = true;
	 	this.data.loaded = true;
	 	this.trigger(this.data);
	 	
	 }
	 else {
	 	api.get_dashboard({id:id})
	 		.then(function (response) {
	 		    console.log(response.objects[0]);
	 			self.data.dashboard = response.objects[0];
	 			self.data.dashboard.charts = response.objects[0].dashboard_json;
	 			self.data.dashboardTitle = 	response.objects[0].title; 			
	 			self.data.loaded = true;
	 			self.trigger(self.data);
	 		}); 
	 }


	},
	setDashboard:function(){
		var date = '2013-03';
		var regionIdx = _.indexBy(this.data.regions, 'id');
		var topLevelRegions = _(this.data.regions)
			.filter(function (r) {
				return !regionIdx.hasOwnProperty(r.parent_region_id);
			})
			.sortBy('name');
		this.data.region = topLevelRegions.first();
		this.data.campaign = _(this.data.campaigns)
				.filter(function (c) {
					return c.office_id === this.data.region.office_id &&
					(!date || _.startsWith(c.start_date, date));
				}.bind(this))
				.sortBy('start_date')
				.last();
		
		this.data.loading = false;
		this.trigger(this.data);
		
		
		
		
	},
	onAddChart:function(chartDef){
	  this.data.dashboard.charts.push(chartDef);
	  DashboardActions.setDashboard({dashboard:this.data.dashboard});
	  this.saveDashboard();
	  this.trigger(this.data);
	},
	onAddDashboard:function(){
	   var data = {
	     title: this.data.dashboardTitle,
	     default_office_id: null,
	     dashboard_json:'[]'
	   };
	   api.save_dashboard(data).then(function(response){
	      if(response.objects.new_id)
	      {
	      	window.location = "/datapoints/dashboard_builder/"+response.objects.new_id;
	      }
	      else {
	      	alert("There was an error saving your chart");
	      }
	   }); 
	},
	saveDashboard:function(){
	    var data = {
	      id: this.data.dashboard.id,
	      description: this.data.dashboard.description,
	      title: this.data.dashboardTitle,
	      default_office_id: null,
	      dashboard_json:JSON.stringify(this.data.dashboard.charts)
	    };
	    api.save_dashboard(data).then(function(response){
	       console.log(response);
	       //self.data.charts = response.objects[0].dashboard_json;
	       //self.trigger(self.data);
	    }); 
	},
	onUpdateChart:function(chartDef,index){
	  this.data.dashboard.charts[index] = chartDef;
	  DashboardActions.setDashboard({dashboard:this.data.dashboard});
	  this.saveDashboard();
	  this.trigger(this.data);
	},
	onUpdateTitle:function(title){
	   this.data.dashboardTitle = title;
	   this.trigger(this.data);
	},
});
	
module.exports = DashboardBuilderStore;