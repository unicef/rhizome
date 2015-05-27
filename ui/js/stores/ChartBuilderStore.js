'use strict';
var Reflux = require('reflux/src');
var ChartBuilderActions = require('actions/ChartBuilderActions');

var _      = require('lodash');
var treeify = require('data/transform/treeify');
var ancestoryString = require('data/transform/ancestryString');
var api = require('data/api');

module.exports = Reflux.createStore({
	data: {
		regionList:[],
		indicatorList:[],
		campaignList:[],
		indicatorsSelected:[],
		regionSelected:null,
		campaignSelected:null,
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
		         			'title'  : indicator.slug,
		         			'value'  : indicator.id,
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
		this.data.indicatorsSelected.push({id:value,
							  title:this._indicatorIndex[value].slug});
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
	}
});

//
