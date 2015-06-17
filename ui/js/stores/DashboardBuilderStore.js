'use strict';

var _      = require('lodash');
var Reflux = require('reflux/src');
var api = require('data/api');

var DashboardBuilderStore = Reflux.createStore({
	listenables : [require('actions/DashboardBuilderActions')],
	getInitialState: function(){
	   return this.data;
	},
	data:{charts:[]},
	onInitialize : function(id){
	var self = this;
	 this.data.dashboardId = id;
		 api.get_dashboard({id:id}).then(function(response){
		    self.data.charts = response.objects[0].dashboard_json;
		    self.trigger(self.data);
		 }); 
	},
	onAddChart:function(chartDef){
	  this.data.charts.push(chartDef);
	  this.trigger(this.data);
	},
	onUpdateChart:function(chartDef,index){
	  this.data.charts[index] = chartDef;
	  this.trigger(this.data);
	}
});
	
module.exports = DashboardBuilderStore;