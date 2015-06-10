var _      = require('lodash');
var d3     = require('d3');
var colors    = require('colors');
var moment = require('moment');
var api = require('data/api');
var Vue = require('vue'); //for tooltip display

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

function seriesObject(d, ind, collection, groups) {
	return {
		name   : groups[ind].name,
		values : d
	};
}

var tooltipDiv = document.createElement('div'); //Vue needs a el to bind to to hold tooltips outside the svg, seems like the least messy solution
document.body.appendChild(tooltipDiv);
var tooltipVue = new Vue({
	el: tooltipDiv,
	components: {'vue-tooltip': require('component/tooltip') },
	ready:function(){

	},
	template: "<vue-tooltip></vue-tooltip>"
});


module.exports = {
	init:function(dataPromise,chartType,indicators,regions,lower,upper,groups,groupBy){
		var indicatorArray = _.map(indicators,_.property('id'));
		var meltPromise = dataPromise.then(function(data){
		 							return melt(data,indicatorArray);
		 							});
		if(chartType=="LineChart"){
		 return	this.processLineChart(meltPromise,lower,upper,groups,groupBy);
		} else if (chartType=="PieChart") {
		 return	this.processPieChart(meltPromise,lower,upper,groups,groupBy);	
		} else if (chartType=="ChoroplethMap") {
		 return	this.processChoroplethMap(meltPromise,regions);	
		} else if (chartType=="ColumnChart") {
		 return	this.processColumnChart(meltPromise,lower,upper);	
		}
	},
	processLineChart:function(dataPromise,lower,upper,groups,groupBy){
		return dataPromise.then(function(data){
			if(!lower) //set the lower bound from the lowest datapoint value
			{
			  var sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'));
			  lower = moment(_.first(sortedDates).campaign.start_date);
			}
			var chartOptions = {
					domain  : _.constant([lower.toDate(), upper.toDate()]),
					aspect : 2.664831804,
					values  : _.property('values'),
					x       : _.property('campaign.start_date'),
					y       : _.property('value'),
					yFormat : d3.format('%')
				}
			var chartData =  _groupBySeries(data, groups,groupBy);
		    return {options:chartOptions,data:chartData};
		}); 	
	},
	processPieChart:function(dataPromise){
		return dataPromise.then(function(data){
			var total = _(data).map(function(n){ return n.value;}).sum();
			var chartOptions = {
					domain  : _.constant([0, total])
				};
			return {options:chartOptions,data:data}; 
		});
	},
	processChoroplethMap:function(dataPromise,regions){
		var regionsIndex = _.indexBy(regions, 'id');
		
		return Promise.all([dataPromise,api.geo({ region__in :_.map(regions,function(region){return region.id}) })])
		.then(_.spread(function(data, border){	
			var index = _.indexBy(data,'region');
			var chartOptions = {
							aspect: 1,
							domain: _.constant([0, 0.1]),
							border: border.objects.features,
							onMouseOver: function (d, el) {
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
							},
							onMouseOut: function (d, el) {
								tooltipVue.$emit('tooltip-hide', { el : el });
							}
							};
		    var chartData = _.map(border.objects.features, function (feature) {
										var region = _.get(index, feature.properties.region_id);
										return _.merge({}, feature, {
												properties : { value : _.get(region, 'value') }
											});
									});
			return {options:chartOptions,data:chartData}; 
		}));
	},
	processColumnChart: function(dataPromise,lower,upper){
		return dataPromise.then(function(data){
			var columnScale = _.map(d3.time.scale()
			  		.domain([lower.valueOf(), upper.valueOf()])
			  		.ticks(d3.time.month, 1),
			  	_.method('getTime')
			  );
			  
			
			//return {options:{},data:[]};
		});
	}
};











   
  
