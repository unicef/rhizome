'use strict';
var Reflux = require('reflux/src');
var ChartBuilderActions = require('actions/ChartBuilderActions');

var _      = require('lodash');
var treeify = require('data/transform/treeify');
var ancestoryString = require('data/transform/ancestryString');
var api = require('data/api');
var d3     = require('d3');
var moment = require('moment');

module.exports = Reflux.createStore({
	data: {
		regionList:[],
		indicatorList:[],
		campaignList:[],
		indicatorsSelected:[{description: "% missed children due to refusal", short_name: "Refused", indicator_bounds: [], id: 166, slug: "-missed-children-due-to-refusal",name: "% missed children due to refusal"}],
		campaignSelected:{office_id: 3, start_date: "2013-09-01", id: 179, end_date: "2013-09-01", slug: "pakistan-september-2013"},
		regionSelected:{id: 12908, title: "Afghanistan"},//{id:null,title:null},
		title: "new chart",
		description: "a nice description",
		regionRadios:[{value:"selected",title:"Selected region only"},{value:"type",title:"Regions with the same type"},{value:"subregions",title:"Subregions 1 level below selected"}],
		regionRadioValue: "selected",
		groupByRadios:[{value:"indicator",title:"Indicators"},{value:"regions",title:"Regions"}],
		groupByRadioValue: "indicator",
		chartTypes:[{name:"line"},{name:"bar"},{name:"graph"},{name:"pie"}],
		selectedChart:"line"
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
	    this.getChartData();
		this.trigger(this.data);
	},
	onRemoveIndicatorSelection: function(id){
	  _.remove(this.data.indicatorsSelected,{id:id});
	  this.trigger(this.data);
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
	},
	onSelectGroupByRadio:function(value){
	   this.data.groupByRadioValue = value;
	   this.trigger(this.data);
	},
	onSelectChart: function(value){
	   this.data.selectedChart = value;
	   this.trigger(this.data);
	},
	onAddCampaignSelection: function(value){
	    //console.log();
		this.data.campaignSelected = this._campaignIndex[value];
		this.trigger(this.data);
	},
	onAddRegionSelection: function(value){
		this.data.regionSelected = {id:value, title:this._regionIndex[value].name};
		this.trigger(this.data);
	},
	getChartData: function(){
		var indicators = this.data.indicatorsSelected;
		
	    var q = {
				indicator__in  : [166],
				region__in     : this.data.regionSelected.id,
				campaign_start : moment(this.data.campaignSelected.start_date).clone().startOf('year').subtract(2, 'years').format('YYYY-MM-DD'),
				campaign_end   : moment(this.data.campaignSelected.end_date).format('YYYY-MM-DD')
	    			};
	    api.datapoints(q).then(function(data){console.log(data);});
	}
});

//
