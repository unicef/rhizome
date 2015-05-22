'use strict';

var _      = require('lodash');
//var moment = require('moment');
var React  = require('react');
//var api = require('data/api');
var treeify = require('../../data/transform/treeify');
var ancestoryString = require('../../data/transform/ancestryString');
var Menu = require('component/menu/menu.jsx');
//var DashboardStore = require('stores/DashboardStore');

var api = require('data/api');


module.exports = React.createClass({
	getInitialState:function(){
	  return {
	    regions:[]
	  }
	},
	componentWillMount: function() {
	   var self = this;
	   api.regions().then(function(items){
	    // self.maps.regions = _.indexBy(items.objects, 'id');
	     var regions = _(items.objects)
	     	.map(function (region) {
	     		return {
	     			'title'  : region.name,
	     			'value'  : region.id,
	     			'id'     : region.id,
	     			'parent' : region.parent_region_id
	     		};
	     	})
	     	.sortBy('title')
	     	.reverse() // I do not know why this works, but it does
	     	.thru(_.curryRight(treeify)('id'))
	     	.thru(ancestoryString)
	     	.value();
	        self.setState({regions:regions});
	    });
	},
	render: function(){
	   return (<div className="visualization-builder-container"> 
	               <form className="inline">
		               <div>
		               		this is the visualization builder
		               </div>
		               <Menu items={this.state.regions}
		                     searchable={true}>
		               		<span style={{width:"200px",display:"inline-block"}}>menu</span>
		               </Menu>
	               </form>
	           </div>
	           );
	}
});