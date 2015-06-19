'use strict';

var _      = require('lodash');
//var moment = require('moment');
var React  = require('react');
var DragDropMixin = require('react-dnd').DragDropMixin;
var Reflux = require('reflux/src');
var ChartBuilder = require('view/chart-builder/ChartBuilder.jsx');

var DataActions = require('actions/DataActions');
var DataStore = require('stores/DataStore');

var DashboardBuilderActions  = require('actions/DashboardBuilderActions');
var DashboardBuilderStore    = require("stores/DashboardBuilderStore");

var RegionTitleMenu     = require('component/RegionTitleMenu.jsx');
var CampaignTitleMenu   = require('component/CampaignTitleMenu.jsx');

module.exports = React.createClass({
	mixins: [Reflux.connect(DashboardBuilderStore,"store"), Reflux.connect(DataStore,"dataStore")],
	
	componentDidMount:function(){
	   console.log(this.props.dashboard_id);
	   DashboardBuilderActions.initialize(this.props.dashboard_id);
	},
	getInitialState:function(){
	  return {
	    chartBuilderActive:false,
	    chartBuilderindex:null
	  }
	},
	editChart:function(index){
	  this.setState({chartBuilderindex : index,chartBuilderActive:true});
	},
	newChart:function(){
	  this.setState({chartBuilderindex : null,chartBuilderActive:true});
	},
	saveChart:function(chartDef){
	    if(!_.isNull(this.state.chartBuilderindex)) //if editing, replace the chart at the index in JSON,
	    {
	      DashboardBuilderActions.updateChart(chartDef,this.state.chartBuilderindex);
	    }
	    else {//add chart
	      DashboardBuilderActions.addChart(chartDef);
	    }
		this.setState({chartBuilderindex : null,chartBuilderActive:false});
	},
   _setCampaign : function (id) {
   
  },
  _setRegion : function (id) {
 
  },
	render: function(){
      var self = this;
      var charts = this.state.store.charts.map(function(chart,index){
          return (
            <div className="vis-box" key={index}>{chart.title}
            <a href="#" onClick={self.editChart.bind(null,index)} className="button">edit chart</a>
            </div>
          );
       }); 
       var campaigns = _(this.state.store.campaigns)
         //.filter(c => c.office_id === region.office_id)
         .sortBy('start_date')
         .reverse()
         .value();
       
       //console.log(this.state.store.campaign,this.state.dashboardStore.region);
       
	   var dashboardBuilderContainer = (
	         <div>
	           <div classNameName='clearfix'></div>
	   
	           <form className='inline no-print'>
	             <div className='row'>
	               <div className='medium-6 columns'>
	                 <h1>
	                   <CampaignTitleMenu
	                     campaigns={campaigns}
	                     selected={this.state.store.campaign}
	                     sendValue={this._setCampaign} />
	                   &emsp;
	                   <RegionTitleMenu
	                     regions={this.state.store.regions}
	                     selected={this.state.store.region}
	                     sendValue={this._setRegion} />
	                 </h1>
	               </div>
	             </div>
	           </form>
	   
	           {charts}
	           <a href="#" onClick={this.newChart} className="button">add chart</a>
	         </div>
	   );
	   if(this.state.store.loading)
	   {
	   	 return (<div>loading</div>);
	   }
	   else if(this.state.chartBuilderActive)
	   {
	    var chartDef = (_.isNull(this.state.chartBuilderindex)?null:this.state.store.charts[this.state.chartBuilderindex]);
	   	return (<ChartBuilder dashboardId={this.props.dashboard_id} chartDef={chartDef} callback={this.saveChart}/>);
	   }
	   else {
	   	return dashboardBuilderContainer;
	   }
	}
});