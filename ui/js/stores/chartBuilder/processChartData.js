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
function nullValuesToZero(values){
  _.each(values,function(value){
  	if(_.isNull(value.value))
  	{
  	  value.value = 0;
  	}
  });
	
}
function _columnData(data, groups, groupBy) {

	var columnData = _(data)
		.groupBy(groupBy)
		.map(_.partialRight(seriesObject, groups))
		.value();
	var largestGroup = [];
	_.each(columnData,function(series){  //The column data is an array of series. Each series has an array of values. Each of the value arrays must be the same length for the stacked column chart to render properly. So first we must loop through all series and find the longest values array, and then pad the remaining arrays with those campaigns to cause the chart to display correctly
	   if(series.values.length > largestGroup.length)
	   {
	     largestGroup = series.values;
	   }
	   _.each(series.values,function(val){
	   	if(_.isNull(val.value))
	   	{
	   	  val.value = 0;
	   	}
	   });
	}); 
	var baseCampaigns = _.map(largestGroup,function(group){
		return group.campaign;
	});
	//console.log(_.map(baseGroup,_.property('campaign.start_date')));
	_.each(columnData,function(series){
	   _.each(baseCampaigns,function(baseCampaign){
	   	   if(!_.find(series.values,function(value){return value.campaign.id == baseCampaign.id}))
	   	   {
	   	     series.values.push({campaign:baseCampaign,region:series.values[0].region,indicator:series.values[0].indicator,value:0});
	   	   }
	   });
//	   var baseGroupValues = _.merge(_.cloneDeep(baseGroup),_.fill(Array(baseGroup.length),{region:series.values[0].region,indicator:series.values[0].indicator}));
//	   series.values = _.assign(baseGroupValues,_.cloneDeep(series.values));
	  // console.log(_.map(series.values,_.property('campaign.start_date')));
	});
    
	var stack = d3.layout.stack()
		.order('default')
		.offset('zero')
		.values(function (d) { return d.values; })
		.x(function (d) { return d.campaign.start_date; })
		.y(function (d) { return d.value; });

	return stack(columnData);
}

module.exports = {
	init:function(dataPromise,chartType,indicators,regions,lower,upper,groups,groupBy){
		var indicatorArray = _.map(indicators,_.property('id'));
		var meltPromise = dataPromise.then(function(data){
		 							return melt(data,indicatorArray);
		 							});
		if(chartType=="LineChart"){
		 return	this.processLineChart(meltPromise,lower,upper,groups,groupBy);
		} else if (chartType=="PieChart") {
		 return	this.processPieChart(meltPromise);	
		} else if (chartType=="ChoroplethMap") {
		 return	this.processChoroplethMap(meltPromise,regions);	
		} else if (chartType=="ColumnChart") {
		 return	this.processColumnChart(meltPromise,lower,upper,groups,groupBy);	
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
	processColumnChart: function(dataPromise,lower,upper,groups,groupBy){
		return dataPromise.then(function(data){
		    if(!lower) //set the lower bound from the lowest datapoint value
		    {
		      var sortedDates = _.sortBy(data, _.method('campaign.start_date.getTime'));
		      lower = moment(_.first(sortedDates).campaign.start_date);
		    }
			var columnScale = _.map(d3.time.scale()
			  		.domain([lower.valueOf(), upper.valueOf()])
			  		.ticks(d3.time.month, 1),
			  	_.method('getTime')
			  );
			  var chartData = _columnData(data,groups,groupBy);	
			
			var chartOptions = {
				aspect : 2.664831804,
				values  : _.property('values'),
				yFormat : d3.format('%'),
				domain : _.constant(columnScale),
				color  : _.flow(
					_.property('name'),
					d3.scale.ordinal().range(colors)),
				x      : function (d) { 
//				              if(!d.campaign)
//				              {
//				                return lower.toDate().getTime();
//				              }
				              var start = d.campaign.start_date
				              return moment(start).startOf('month').toDate().getTime(); 
				              },
				xFormat: function (d) { return moment(d).format('MMM YYYY')}
			};  		
			return {options:chartOptions,data:chartData}; 
			
		});
	},
	processScatterChart: function(dataPromise){
		return dataPromise.then(function(data){
					
			return {options:{},data:[]}; 
		});
	}
};











   
  
