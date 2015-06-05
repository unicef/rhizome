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
function _conversions(data, indicators) {
	return _(data)
		.groupBy('indicator')
		.map(function (d, ind) {
			return seriesObject(
				_.sortBy(d, _.method('campaign.start_date.getTime')),
				ind,
				null,
				indicators
			);
		})
		.value();
}
function seriesObject(d, ind, collection, indicators) {
	return {
		name   : indicators[ind].short_name,
		values : d
	};
}
var canDisplayChart = function(){
	if(this.indicatorsSelected.length > 0)
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
		regionSelected:{id: 12908, title: "Afghanistan"},//{id:null,title:null},
		title: "new chart",
		description: "a nice description",
		regionRadios:[{value:"selected",title:"Selected region only"},{value:"type",title:"Regions with the same type"},{value:"subregions",title:"Subregions 1 level below selected"}],
		regionRadioValue: "selected",
		groupByRadios:[{value:"indicator",title:"Indicators"},{value:"regions",title:"Regions"}],
		groupByRadioValue: "indicator",
		chartTypes:[{name:"line"},{name:"bar"},{name:"graph"},{name:"pie"}],
		selectedChart:"line",
		chartData:[],
	    chartOptions : {
				aspect  : 2.664831804,
				domain  : null,
				values  : _.property('values'),
				x       : _.property('campaign.start_date'),
				y       : _.property('value'),
				yFormat : d3.format(',.0f')
			},
		canDisplayChart:canDisplayChart
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
		  	.map(ancestoryString)
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

		Promise.all([api.campaign(), api.office()])
			.then(_.spread(function(campaigns, offices) {
				var officeIdx = _.indexBy(offices.objects, 'id');

				self.data.campaignList = _(campaigns.objects)
					.map(function (campaign) {
						return _.assign({}, campaign, {
							'start_date' : moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
							'end_date'   : moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
							'office'     : officeIdx[campaign.office_id]
						});
					})
					.sortBy(_.method('start_date.getTime'))
					.reverse()
					.value();

				self._campaignIndex = _.indexBy(self.data.campaignList, 'id');

				self.trigger(self.data);
			}));
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
		this.data.campaignSelected = this._campaignIndex[value];
		this.trigger(this.data);
	},
	onAddRegionSelection: function(value){
		this.data.regionSelected = {id:value, title:this._regionIndex[value].name};
		this.trigger(this.data);
	},
	getChartData: function(){
		var self = this;
		var indicators = _.indexBy(this.data.indicatorsSelected, 'id');//;
		var start = moment(this.data.campaignSelected.end_date);
		var meltObjects  = _.flow(_.property('objects'), melt);
		var lower = start.clone().startOf('month').subtract(1, 'year');
		var upper = start.clone().endOf('month');
		this.data.chartOptions.domain = _.constant([lower.toDate(), upper.toDate()]);

	    var q = {
		indicator__in  : _.map(this.data.indicatorsSelected,function(indicator){return indicator.id}),
		region__in     : this.data.regionSelected.id,
		campaign_start : lower.format('YYYY-MM-DD'),
		campaign_end   : upper.format('YYYY-MM-DD')
	    			};
	    api.datapoints(q).then(meltObjects).then(function(data){
	    	self.data.chartData =  _conversions(data, indicators);
	    	console.log(self.data.chartData);
	    	self.trigger(self.data);
	    });
	}
});
