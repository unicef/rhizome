'use strict';

var React  = require('react');
var Reflux = require('reflux/src');
var Menu = require('component/menu/menu.jsx');
var List = require('component/list/List.jsx');
var RadioGroup = require('component/radio-group/RadioGroup.jsx');
var ChartSelect = require('./ChartSelect.jsx');
var ChartBuilderStore = require("stores/ChartBuilderStore");
var ChartBuilderActions = require('actions/ChartBuilderActions');

module.exports = React.createClass({
    mixins: [Reflux.connect(ChartBuilderStore,"store")],
	getDefaultProps:function(){
	  return {
	    showRegionRadio:[{value:"selected",title:"Selected region only"},{value:"type",title:"Regions with the same type"},{value:"subregions",title:"Subregions 1 level below selected"}]
	  }
	},
    _updateTitle: function(e){
      ChartBuilderActions.updateTitle(e.target.value);
    },
    _updateDescription: function(e){
      ChartBuilderActions.updateDescription(e.target.value);
    },
	render: function(){
	   return (<form className="inline">  
	           <div className="visualization-builder-container"> 
	              <div className="left-page">
	                   <div className="titleDiv">Title</div>
	                   <input type="text" value={this.state.store.title} onChange={this._updateTitle}/>
	                   <div className="titleDiv" onChange={this._updateDescription}>Description</div>
	                   <textarea value={this.state.store.description} onChange={this._updateDescription}></textarea>
	                   <div className="titleDiv">Indicators</div>
	                   <Menu items={this.state.store.indicatorList}
		                     sendValue={ChartBuilderActions.addIndicatorSelection}
		                     searchable={true}>
		               		<span className="ChartBuilderInidcatorButton">Select Indicators</span>
		               </Menu>
		               <List items={this.state.store.indicatorsSelected} removeItem={ChartBuilderActions.removeIndicatorSelection} />
		               <div className="titleDiv">Show</div>
                       <RadioGroup name="show" value={this.state.store.regionRadioValue} values={this.props.showRegionRadio} onChange={ChartBuilderActions.selectShowRegionRadio} />
	              </div> 
	              <div className="right-page">
	              	<ChartSelect charts={this.state.store.chartTypes} value={this.state.store.selectedChart} onChange={ChartBuilderActions.selectChart} />
	              </div>
	            </div>
	            </form>
	           );
	}
});