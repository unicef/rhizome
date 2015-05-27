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
		indicatorsSelected:[],
		title: "new chart",
		description: "a nice description",
		regionRadioValue: "selected",
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
	updateTitle:function(value){
	   this.data.title = value;
	   this.trigger(this.data);
	},
	updateDescription:function(value){
	   this.data.description = value;
	   this.trigger(this.data);
	},
	selectShowRegionRadio:function(value){
	   this.data.regionRadioValue = value;
	   this.trigger(this.data);
	},
	onSelectChart: function(value){
	   this.data.selectedChart = value;
	   this.trigger(this.data);
	}
});

//
