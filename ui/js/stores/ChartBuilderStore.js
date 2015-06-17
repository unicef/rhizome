'use strict';
var Reflux = require('reflux/src');
var ChartBuilderActions = require('actions/ChartBuilderActions');

var _      = require('lodash');
var treeify = require('data/transform/treeify');
var ancestoryString = require('data/transform/ancestryString');
var api = require('data/api');
var d3     = require('d3');
var moment = require('moment');
var colors    = require('colors');
var Vue = require('vue'); //for tooltip display
var processChartData = require('./chartBuilder/processChartData');


function melt(data,indicatorArray) {
	var dataset = data.objects;
	var baseIndicators = _.map(indicatorArray,function(indicator){
		return {indicator:indicator+'',value:0};
	});
	var o = _(dataset)
		.map(function (d) {
			var base = _.omit(d, 'indicators');
			var indicatorFullList = _.assign(_.cloneDeep(baseIndicators),d.indicators);
			return _.map(indicatorFullList, function (indicator) {
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
var canDisplayChartReason = function(){
	var reason;
	if(this.indicatorsSelected.length == 0)
	{
	  reason = "Please select at least one indicator";
	}
	else if(!this.campaignSelected.id){
	  reason = "Please select a campaign";
	}
	else if(this.chartData.length == 0)
	{
	  reason = "No data to display";
	}
	else {
		reason = '';
	}
	return reason;
};

function _columnData(data, groups, groupBy) {

	var columnData = _(data)
		.groupBy(groupBy)
		.map(_.partialRight(seriesObject, groups))
		.value();
	var largestGroup = [];
	_.each(columnData,function(series){
	   if(series.values.length > largestGroup.length)
	   {
	     largestGroup = series.values;
	   }
	});
	var baseGroup = _.map(largestGroup,function(group){
		return {campaign:group.campaign,
				value:0,y:0,y0:0};
	});
	_.each(columnData,function(series){
	   
	   var baseGroupValues = _.merge(_.cloneDeep(baseGroup),_.fill(Array(baseGroup.length),{region:series.values[0].region,indicator:series.values[0].indicator}));
	   series.values = _.assign(baseGroupValues,_.cloneDeep(series.values));
	});

	var stack = d3.layout.stack()
		.order('default')
		.offset('zero')
		.values(function (d) { return d.values; })
		.x(function (d) { return d.campaign.start_date; })
		.y(function (d) { return d.value; });

	return stack(columnData);
}


	
var chartOptions = {
		domain  : null,
		values  : _.property('values'),
		x       : _.property('campaign.start_date'),
		y       : _.property('value'),
		yFormat : d3.format('%')
	};
module.exports = Reflux.createStore({
	data: {
		regionList:[],
		indicatorList:[],
		campaignList:[],
		indicatorsSelected:[{description: "% missed children due to refusal", short_name: "Refused", indicator_bounds: [], id: 166, slug: "-missed-children-due-to-refusal",name: "% missed children due to refusal"}],
		campaignSelected:{office_id: 2, start_date: "2014-02-01", id: 137, end_date: "2014-02-01", slug: "afghanistan-february-2014"},
		regionSelected:{parent_region_id: null, office_id: 1, region_type_id: 1, id: 12907, name: "Nigeria"},//{id:null,title:null},
		aggregatedRegions:[],
		title: "new chart",
		description: "a nice description",
		regionRadios:[{value:"selected",title:"Selected region only"},{value:"type",title:"Regions with the same type"},{value:"subregions",title:"Subregions 1 level below selected"}],
		regionRadioValue: 2,
		groupByRadios:[{value:"indicator",title:"Indicators"},{value:"region",title:"Regions"}],
		groupByRadioValue: 1,
		timeRadios:function(){
		            var self = this;
		            var radios = [{value:"allTime",title:"All Time"},{value:"pastYear",title:"Past Year"},{value:"3Months",title:"Past 3 Months"},{value:"current",title:"Current Campaign"}];
		            var timeRadios = _.filter(radios,function(radio){ return self.chartTypes[self.selectedChart].timeRadios.indexOf(radio.value)>-1; });
		            if(timeRadios.length -1 < this.timeRadioValue)
		            {
		              this.timeRadioValue = 0;
		            }
		            return timeRadios;
					},
		timeRadioValue:2,
		chartTypes:require('./chartBuilder/chartDefinitions'),
		selectedChart:0,
		chartData:[],
	    chartOptions : chartOptions,
		canDisplayChart:canDisplayChart,
		canDisplayChartReason:canDisplayChartReason,
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
		  	.map(ancestoryString)
		  	.value();
		  	self.trigger(self.data);
		  	self.aggregateRegions();
		 });

		 api.indicatorsTree().then(function(items) {
		        self._indicatorIndex = _.indexBy(items.flat, 'id');
		        self.data.indicatorList = _(items.objects)
		         	.sortBy('title')
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
	   //this.data.chartOptions = chartOptions;
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
	    var regionRadioValue = this.data.regionRadios[this.data.regionRadioValue].value;
	    if(regionRadioValue==="selected")
	    {
    	   regions = [regionSelected];
	    }
		else if(regionRadioValue==="type")
		{  
		   if(regionSelected.parent_region_id && regionSelected.parent_region_id != "None")
		   {
		     regions = _.filter(this._regionIndex, {region_type_id:regionSelected.region_type_id,office_id:regionSelected.office_id});
		   }
		   else {
		   	 regions = _.filter(this._regionIndex, {region_type_id:this.data.regionSelected.region_type_id});
		   }
		}
		else if(regionRadioValue==="subregions")
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
	    var range = this.data.timeRadios()[this.data.timeRadioValue].value;
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
	    var selectedChart = this.data.chartTypes[this.data.selectedChart].name;
	    var groupBy = this.data.groupByRadios[this.data.groupByRadioValue].value;
	    var self = this;
		var indicatorsIndex = _.indexBy(this.data.indicatorsSelected, 'id');//;
		var regionsIndex = _.indexBy(this.data.aggregatedRegions, 'id');
		var groups = (groupBy == 'indicator'?indicatorsIndex:regionsIndex);
		var start = moment(this.data.campaignSelected.start_date);
		var meltObjects  = _.flow(_.property('objects'), melt);
		var lower = this.getLower(start);//.subtract(1, 'year');
		var upper = start.clone().startOf('month');
        var indicatorArray = _.map(this.data.indicatorsSelected,_.property('id'))
	    var q = {
		indicator__in  : indicatorArray,
		region__in     : _.map(this.data.aggregatedRegions,_.property('id')),
		campaign_start : (lower?lower.format('YYYY-MM-DD'):null),
		campaign_end   : upper.format('YYYY-MM-DD')
	    			};
       
       
        processChartData
        .init(api.datapoints(q),selectedChart,this.data.indicatorsSelected,this.data.aggregatedRegions,lower,upper,groups,groupBy)
        .then(function(chart){
          self.data.loading = false;
          self.data.chartOptions = chart.options;
          self.data.chartData = chart.data;
          self.trigger(self.data);
        });
       /*  
	    var dataPointPromise = api.datapoints(q).then(function(data){
	    							return melt(data,indicatorArray);}
	    							).then(function(data){
	        if(!lower) //set the lower bound from the lowest datapoint value
	        {
	          var sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'));
	          lower = moment(_.first(sortedDates).campaign.start_date);
	          //var end = moment(_.last(sortedDates).campaign.end_date);
	        }
	        if(selectedChart ==="LineChart")
	        {
	          self.data.chartOptions.aspect = 2.664831804;
	          self.data.chartOptions.domain = _.constant([lower.toDate(), upper.toDate()]);
	    	  self.data.chartData =  _groupBySeries(data, groups,groupBy);
	    	}
	    	else if (selectedChart ==="PieChart"){
	    	  var total = _(data).map(function(n){ return n.value;}).sum();
	    	  self.data.chartOptions.domain = _.constant([0, total]);
	    	  self.data.chartOptions.color = _.flow(
	    	  	_.property('name'),
	    	  	d3.scale.ordinal().range(colors));
	    	  self.data.chartData = data;
	    	}
	    	else if (selectedChart ==="ColumnChart"){
		  			
		  	  var columnScale = _.map(d3.time.scale()
		  	  		.domain([lower.valueOf(), upper.valueOf()])
		  	  		.ticks(d3.time.month, 1),
		  	  	_.method('getTime')
		  	  );
		  	  var chartData = _columnData(data,groups,groupBy);	
		  	  		
		  	  self.data.chartOptions.aspect = 2.664831804;
	    	  self.data.chartOptions.domain = _.constant(columnScale);
	    	  self.data.chartOptions.color = _.flow(
	    	  	_.property('name'),
	    	  	d3.scale.ordinal().range(colors));
	    	  self.data.chartOptions.x = function (d) { 
	    	  return moment(d.campaign.start_date).startOf('month').toDate().getTime(); };
	    	  self.data.chartOptions.xFormat = function (d) { return moment(d).format('MMM YYYY')};
	    	  self.data.chartData = chartData;
	    	}
	    	self.data.loading = false;
	    	self.trigger(self.data);
	    	return data; //return data for dataPointPromise for cooridnating with charts that need multiple datasets
	    });
	    
	    if(selectedChart ==="ChoroplethMap")
	    {
		    Promise.all([dataPointPromise,api.geo({ region__in :_.map(this.data.aggregatedRegions,function(region){return region.id}) })])
		    .then(_.spread(function(data, border){
		        var index = _.indexBy(data,'region');
		        self.data.chartOptions.aspect = 1;
		        self.data.chartOptions.domain = _.constant([0, 0.1]);
				self.data.chartOptions.border = border.objects.features;
				self.data.chartOptions.onMouseOver = function (d, el) {
				    if (regionsIndex.hasOwnProperty(d.properties.region_id)) {
						var evt = d3.event;
						tooltipVue.$emit('tooltip-show', {
							el       : el,
							position : {
								x : evt.pageX,
								y : evt.pageY
							},
							data : {
								text     : regionsIndex[d.properties.region_id].name,
								template : 'tooltip-default'
							}
						});
					}
				};
				self.data.chartOptions.onMouseOut = function (d, el) {
					tooltipVue.$emit('tooltip-hide', { el : el });
				}
				
                self.data.chartData = _.map(border.objects.features, function (feature) {
                							var region = _.get(index, feature.properties.region_id);
                							return _.merge({}, feature, {
                									properties : { value : _.get(region, 'value') }
                								});
                						});
                self.data.loading = false;
                self.trigger(self.data);
           }));
	    }
	    */
	}
});
