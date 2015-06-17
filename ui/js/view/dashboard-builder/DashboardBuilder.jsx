'use strict';

var _      = require('lodash');
//var moment = require('moment');
var React  = require('react');
var DragDropMixin = require('react-dnd').DragDropMixin;
var DashboardBuilderActions  = require('actions/DashboardBuilderActions');
var DashboardBuilderStore    = require("stores/DashboardBuilderStore");
var Reflux = require('reflux/src');
var ChartBuilder = require('view/chart-builder/ChartBuilder.jsx');

//var DashboardStore = require('stores/DashboardStore');

module.exports = React.createClass({
	mixins: [Reflux.connect(DashboardBuilderStore,"store")],
	componentDidMount:function(){
	   DashboardBuilderActions.initialize(this.props.dashboard_id);
	},
	getInitialState:function(){
	  return {
	    visualizations:[{id:1},{id:2},{id:3},{id:4},{id:5},{id:6}],
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
	render: function(){
      var self = this;
      var charts = this.state.store.charts.map(function(chart,index){
          return (
            <div className="vis-box" key={index}>{chart.title}
            <a href="#" onClick={self.editChart.bind(null,index)} className="button">edit chart</a>
            </div>
          );
       }); 
	   var dashboardBuilderContainer = (<form className="inline  dashboard-builder-container">
	   			{charts}
	   			<a href="#" onClick={this.newChart} className="button">add chart</a>
	   		   </form>);
	   if(this.state.chartBuilderActive)
	   {
	    var chartDef = (_.isNull(this.state.chartBuilderindex)?null:this.state.store.charts[this.state.chartBuilderindex]);
	   	return (<ChartBuilder dashboardId={this.props.dashboard_id} chartDef={chartDef} callback={this.saveChart}/>);
	   }
	   else {
	   	return dashboardBuilderContainer;
	   }
	}
});