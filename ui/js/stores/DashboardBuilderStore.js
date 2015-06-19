'use strict';

var _      = require('lodash');
var Reflux = require('reflux/src');
var api = require('data/api');

var treeify = require('data/transform/treeify');
var ancestoryString = require('data/transform/ancestryString');
var moment = require('moment');

var DashboardBuilderStore = Reflux.createStore({
	listenables : [require('actions/DashboardBuilderActions')],
	getInitialState: function(){
	   return this.data;
	},
	data:{charts:[],
	      regions:[],
	      campaigns:[],
	      indicators:{},
	      loading:true},
	onInitialize : function(id){
	var self = this;
	 this.data.dashboardId = id;

		Promise.all([api.regions(), api.campaign(),api.get_dashboard({id:id})])
			.then(function (responses) {
				self.data.regions    = responses[0].objects;
				self.data.campaigns  = responses[1].objects;
				self.data.charts = responses[2].objects[0].dashboard_json;
				_.each(self.data.charts,function(chart){
					self.addChartDefinition(chart);
				});
				self.data.dashboard = responses[2].objects[0];
				self.setDashboard();
			}); 
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
	addChartDefinition : function (chart) {
		var base = _.omit(chart, 'indicators', 'title');
		_.each(chart.indicators, function (id) {
			var duration = moment.duration(chart.timeRange);
			var hash     = [id, chart.startOf, chart.region].join('-');

			if (!this.data.indicators.hasOwnProperty(hash) || duration > this.data.indicators[hash].duration) {
				this.data.indicators[hash] = _.assign({
						duration   : duration,
						indicators : [id]
					}, base);
			}
		}.bind(this));
	},
	onAddChart:function(chartDef){
	  this.data.charts.push(chartDef);
	  this.saveDashboard();
	  this.trigger(this.data);
	},
	saveDashboard:function(){
	    var data = {
	      id: this.data.dashboard.id,
	      description: this.data.dashboard.description,
	      title: this.data.dashboard.title,
	      default_office_id: this.data.dashboard.default_office_id,
	      dashboard_json:JSON.stringify(this.data.charts)
	    };
	    api.save_dashboard(data).then(function(response){
	       console.log(response);
	       //self.data.charts = response.objects[0].dashboard_json;
	       //self.trigger(self.data);
	    }); 
	},
	onUpdateChart:function(chartDef,index){
	  this.data.charts[index] = chartDef;
	  this.saveDashboard();
	  this.trigger(this.data);
	}
});
	
module.exports = DashboardBuilderStore;