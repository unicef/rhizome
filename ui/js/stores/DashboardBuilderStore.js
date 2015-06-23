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
	      dashboardDescription:''
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
	 			self.data.dashboardDescription = response.objects[0].description;
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
	  chartDef.id = chartDef.title + (new Date()).valueOf();
	  this.data.dashboard.charts.push(chartDef);
	  DashboardActions.setDashboard({dashboard:this.data.dashboard});
	  this.saveDashboard();
	  this.trigger(this.data);
	},
	onRemoveChart:function(index){
	  this.data.dashboard.charts.splice(index, 1);
	  DashboardActions.setDashboard({dashboard:this.data.dashboard});
	  this.saveDashboard();
	  this.trigger(this.data);
	},
	onMoveForward:function(index){
	  console.log('forward');
	  var newIndex;
	  if(index==this.data.dashboard.charts.length -1)
	  {
	    newIndex = 0;
	  }
	  else {
	  	newIndex = index + 1;
	  }
	  var temp = this.data.dashboard.charts[index];
	  this.data.dashboard.charts[index] = this.data.dashboard.charts[newIndex];
	  this.data.dashboard.charts[newIndex] = temp;
	  this.saveDashboard()
	  this.trigger(this.data);
	},  
    onMoveBackward:function(index){
      var newIndex;
      if(index==0)
      {
        newIndex = this.data.dashboard.charts.length -1;
      }
      else {
      	newIndex = index - 1;
      }
      var temp = this.data.dashboard.charts[index];
      this.data.dashboard.charts[index] = this.data.dashboard.charts[newIndex];
      this.data.dashboard.charts[newIndex] = temp;
      this.saveDashboard()
      this.trigger(this.data);
    },  
    onDeleteDashboard:function(){
       var data = {
         description: this.data.dashboardDescription,
         title: this.data.dashboardTitle,
         default_office_id: null,
         dashboard_json:JSON.stringify(this.data.dashboard.charts)
       };
       console.log(this.data.dashboard);
       delete this.data.dashboard.charts;
       var dj = JSON.stringify(this.data.dashboard.dashboard_json);
       this.data.dashboard.id = '';
       
       api.save_dashboard({id:'',title:this.data.dashboard.title}).then(function(response){
          window.location = '/';
       });
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
	      	window.location = "/datapoints/dashboards/edit/"+response.objects.new_id;
	      }
	      else {
	      	alert("There was an error saving your chart");
	      }
	   });
	},
	saveDashboard:function(){
	    var data = {
	      id: this.data.dashboard.id,
	      description: this.data.dashboardDescription,
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
	   clearTimeout(this.timer);
	   if(this.data.dashboard)
	   {
	     this.timer = setTimeout(function(){this.saveDashboard()}.bind(this), 1000);
	   }
	},
	onUpdateDescription:function(description){
	   this.data.dashboardDescription = description;
	   this.trigger(this.data);
	   
	   clearTimeout(this.timer);
	   this.timer = setTimeout(function(){this.saveDashboard()}.bind(this), 1000);
	},
});

module.exports = DashboardBuilderStore;
