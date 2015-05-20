'use strict';

var _      = require('lodash');
//var moment = require('moment');
var React  = require('react');
var DragDropMixin = require('react-dnd').DragDropMixin;
//var api = require('data/api');

//var DashboardStore = require('stores/DashboardStore');

module.exports = React.createClass({
	getInitialState:function(){
	  return {
	    visualizations:[{id:1},{id:2},{id:3},{id:4},{id:5},{id:6}]
	  }
	},
	render: function(){
       var boxes = this.state.visualizations.map(function(visualization){
          return (
            <div className="vis-box" key={visualization.id}>{visualization.id}</div>
          );
       }); 
	   return (<div className="dashboard-builder-container">{boxes}</div>);
	}
});