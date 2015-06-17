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
	    chartBuilderId:null
	  }
	},
	editChart:function(index){
	 console.log(index);
	  this.setState({chartBuilderId : index,chartBuilderActive:true});
	},
	render: function(){
      var self = this;
      
      
      
       var charts = this.state.store.charts.map(function(chart,index){
          console.log(chart);
          return (
            <div className="vis-box" key={index}>{chart.title}
            <a href="#" onClick={self.editChart.bind(null,index)} className="button">edit chart</a>
            </div>
          );
       }); 
	   var dashboardBuilderContainer = (<form className="inline  dashboard-builder-container">
	   			{charts}
	   			<a href={"/datapoints/chart_builder/"+this.props.dashboard_id} className="button">add chart</a>
	   		   </form>);
	   if(this.state.chartBuilderActive)
	   {
	   	return (<ChartBuilder dashboardId={this.props.dashboard_id} chartId={this.props.chartBuilderId} />);
	   }
	   else {
	   	return dashboardBuilderContainer;
	   }
	}
});