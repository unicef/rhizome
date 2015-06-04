'use strict';
var Reflux = require('reflux/src');
var ChartBuilderActions = require('actions/ChartBuilderActions');

var _      = require('lodash');
var treeify = require('data/transform/treeify');
var ancestoryString = require('data/transform/ancestryString');
var api = require('data/api');
var d3     = require('d3');
var moment = require('moment');

function melt(dataset) {
	var o = _(dataset)
		.map(function (d) {
			var base = _.omit(d, 'indicators');

			return _.map(d.indicators, function (indicator) {
				return _.assign({}, base, indicator);
			});
		})
		.flatten()
		.value();

	return o;
}
function _groupBySeries(data, groups,groupBy) {
	return _(data)
		.groupBy(groupBy)
		.map(function (d, ind) {
			return seriesObject(
				_.sortBy(d, _.method('campaign.start_date.getTime')),
				ind,
				null,
				groups
			);
		})
		.value();
}
function seriesObject(d, ind, collection, indicators) {
	return {
		name   : indicators[ind].name,
		values : d
	};
}
var canDisplayChart = function(){
	if(this.indicatorsSelected.length > 0 && this.campaignSelected.id && this.chartData.length > 0)
	{
	  return true;
	}
	else {
		return false;
	}
};
module.exports = Reflux.createStore({
	data: {
		regionList:[],
		indicatorList:[],
		campaignList:[],
		indicatorsSelected:[{description: "% missed children due to refusal", short_name: "Refused", indicator_bounds: [], id: 166, slug: "-missed-children-due-to-refusal",name: "% missed children due to refusal"}],
		campaignSelected:{office_id: 2, start_date: "2014-02-01", id: 137, end_date: "2014-02-01", slug: "afghanistan-february-2014"},
		regionSelected:{parent_region_id: null, office_id: 2, region_type_id: 1, id: 12908, name: "Afghanistan"},//{id:null,title:null},
		aggregatedRegions:[],
		title: "new chart",
		description: "a nice description",
		regionRadios:[{value:"selected",title:"Selected region only"},{value:"type",title:"Regions with the same type"},{value:"subregions",title:"Subregions 1 level below selected"}],
		regionRadioValue: "selected",
		groupByRadios:[{value:"indicator",title:"Indicators"},{value:"region",title:"Regions"}],
		groupByRadioValue: "region",
		timeRadios:[{value:"allTime",title:"All Time"},{value:"pastYear",title:"Past Year"},{value:"3Months",title:"Past 3 Months"},{value:"current",title:"Current Campaign"}],
		timeRadioValue:"current",
		chartTypes:[{name:"LineChart"},{name:"PieChart"},{name:"ChoroplethMap"}],
		selectedChart:"ChoroplethMap",
		chartData:[],
	    chartOptions : {
				domain  : null,
				values  : _.property('values'),
				x       : _.property('campaign.start_date'),
				y       : _.property('value'),
				yFormat : d3.format('%')
			},
		canDisplayChart:canDisplayChart,
		loading:false
	},
	listenables: [ChartBuilderActions],
	getInitialState: function(){
	   return this.data;
	},
	init: function(){
		var self = this;
		api.regions().then(function(items){
		  self._regionIndex = _.indexBy(items.objects, 'id');
		  self.data.regionList = _(items.objects)
		  	.map(function (region) {
		  		return {
		  			'title'  : region.name,
		  			'value'  : region.id,
		  			'parent' : region.parent_region_id
		  		};
		  	})
		  	.sortBy('title')
		  	.reverse() // I do not know why this works, but it does
		  	.thru(_.curryRight(treeify)('value'))
		  	.thru(ancestoryString)
		  	.value();
		  	self.trigger(self.data);
		  	self.aggregateRegions();
		 });
		 api.indicators().then(function(items){
		        self._indicatorIndex = _.indexBy(items.objects, 'id');
		        self.data.indicatorList = _(items.objects)
		         	.map(function (indicator) {
		         		return {
		         			'title'  : indicator.name,
		         			'value'  : indicator.id,
		         			'parent' : null
		         		};
		         	})
		         	.sortBy('title')
		         	.reverse() 
		         	.value();
		         self.trigger(self.data);
		     });
		 api.campaign().then(function(items){
		        self._campaignIndex = _.indexBy(items.objects, 'id');
		        self.data.campaignList = _(items.objects)
		         	.map(function (campaign) {
		         		return {
		         			'title'  : campaign.slug,
		         			'value'  : campaign.id,
		         			'parent' : null
		         		};
		         	})
		         	.sortBy('title')
		         	.reverse() 
		         	.value();
		         self.trigger(self.data);
		     });
	},
	onAddIndicatorSelection: function(value){
		this.data.indicatorsSelected.push(this._indicatorIndex[value]);
	    this.trigger(this.data);
		this.getChartData();
	},
	onRemoveIndicatorSelection: function(id){
	  _.remove(this.data.indicatorsSelected,{id:id});
	  this.trigger(this.data);
	  this.getChartData();
	},
	onUpdateTitle:function(value){
	   this.data.title = value;
	   this.trigger(this.data);
	},
	onUpdateDescription:function(value){
	   this.data.description = value;
	   this.trigger(this.data);
	},
	onSelectShowRegionRadio:function(value){
	   this.data.regionRadioValue = value;
	   this.trigger(this.data);
	   this.aggregateRegions();
	},
	onSelectGroupByRadio:function(value){
	   this.data.groupByRadioValue = value;
	   this.trigger(this.data);
	   this.getChartData();
	},
	onSelectTimeRadio:function(value){
	   this.data.timeRadioValue = value;
	   this.trigger(this.data);
	   this.getChartData();
	},	
	onSelectChart: function(value){
	   this.data.selectedChart = value;
	   this.data.chartData = [];
	   this.trigger(this.data);
	   this.getChartData();
	},
	onAddCampaignSelection: function(value){
		this.data.campaignSelected = this._campaignIndex[value];
		this.trigger(this.data);
		this.getChartData();
	},
	onAddRegionSelection: function(value){
		this.data.regionSelected = this._regionIndex[value];
		this.trigger(this.data);
		this.aggregateRegions();
	},
	aggregateRegions: function(){
	    var regions;
	    var regionSelected = this.data.regionSelected;
	    if(this.data.regionRadioValue==="selected")
	    {
    	   regions = [regionSelected];
	    }
		else if(this.data.regionRadioValue==="type")
		{ 
		   
		   if(regionSelected.parent_region_id)
		   {
		     regions = _.filter(this._regionIndex, {region_type_id:regionSelected.region_type_id,office_id:regionSelected.office_id});
		   }
		   else {
		   	 regions = _.filter(this._regionIndex, {region_type_id:this.data.regionSelected.region_type_id});
		   }
		}
		else if(this.data.regionRadioValue==="subregions")
		{
		   regions = _.filter(this._regionIndex, {parent_region_id:regionSelected.id});
		}
		this.data.aggregatedRegions = regions;
		if(this.canFetchChartData())
		{
			this.getChartData();
		}
	},
	canFetchChartData : function(){
		if(this.data.indicatorsSelected.length > 0 && this.data.campaignSelected.id)
		{
		  return true;
		}
		else {
			return false;
		}
	},
	//Since upper is always the end of the month for the given campaign, it doesn't need it's on compute function, but the lower bound changes based on the time radios the are selected
	getLower:  function(start){
	    var range = this.data.timeRadioValue;
	    if(range=="current"){
	    	return start.clone().startOf('month');
	    } else if (range=="3Months"){
	    	return start.clone().startOf('month').subtract(3,'month');
	    } else if (range=="pastYear"){
	    	return start.clone().startOf('month').subtract(1,'year');
	    } else if (range=="allTime"){
	    	return null;
	    }
	},
	getChartData: function(){
	    this.data.loading = true;
	    this.trigger(this.data); //send the loading parameter to the view
	    var self = this;
		var indicatorsIndex = _.indexBy(this.data.indicatorsSelected, 'id');//;
		var regionsIndex = _.indexBy(this.data.aggregatedRegions, 'id');
		var groups = (this.data.groupByRadioValue == 'indicator'?indicatorsIndex:regionsIndex);
		var start = moment(this.data.campaignSelected.start_date);
		var meltObjects  = _.flow(_.property('objects'), melt);
		var lower = this.getLower(start);//.subtract(1, 'year');
		var upper = start.clone().startOf('month');

	    var q = {
		indicator__in  : _.map(this.data.indicatorsSelected,function(indicator){return indicator.id}),
		region__in     : _.map(this.data.aggregatedRegions,function(region){return region.id}),
		campaign_start : (lower?lower.format('YYYY-MM-DD'):null),
		campaign_end   : upper.format('YYYY-MM-DD')
	    			};
	    
	    var dataPointPromise = api.datapoints(q).then(meltObjects).then(function(data){
	        if(!lower) //set the lower bound from the lowest datapoint value
	        {
	          var sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'));
	          lower = moment(_.first(sortedDates).campaign.start_date);
	          //var end = moment(_.last(sortedDates).campaign.end_date);
	        }
	        if(self.data.selectedChart ==="LineChart")
	        {
	          self.data.chartOptions.aspect = 2.664831804;
	          self.data.chartOptions.domain = _.constant([lower.toDate(), upper.toDate()]);
	    	  self.data.chartData =  _groupBySeries(data, groups,self.data.groupByRadioValue);
	    	}
	    	else if (self.data.selectedChart ==="PieChart"){
	    	  
	    	  
	    	  var total = _.reduce(data,function(total,n){ return total + n.value},0);
	    	  self.data.chartOptions.domain = _.constant([0, total]);
	    	  self.data.chartData = _.filter(data,function(n){ return n.value});
	    	  
	    	}
	    	//self.data.loading = false;
	    	self.trigger(self.data);
	    	return data; //return data for dataPointPromise for cooridnating with charts that need multiple datasets
	    });
	    
	    if(self.data.selectedChart ==="ChoroplethMap")
	    {
		    Promise.all([dataPointPromise,api.geo({ region__in :_.map(this.data.aggregatedRegions,function(region){return region.id}) })])
		    .then(_.spread(function(data, border){
		        var index = _.indexBy(data,'region');
		        self.data.chartOptions.aspect = 1;
		        self.data.chartOptions.domain = _.constant([0, 0.1]);
				self.data.chartOptions.border = border.objects.features;		        
                self.data.chartData = _.map(border.objects.features, function (feature) {
                							var region = _.get(index, feature.properties.region_id);
                							return _.merge({}, feature, {
                									properties : { value : _.get(region, 'value') }
                								});
                						});
                //self.data.loading = false;
                self.trigger(self.data);
           }));
	    }
	}
});
