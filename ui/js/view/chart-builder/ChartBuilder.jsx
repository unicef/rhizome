'use strict';

var React  = require('react');
var Reflux = require('reflux/src');
var Menu = require('component/menu/menu.jsx');
var List = require('component/list/List.jsx');
var RadioGroup = require('component/radio-group/RadioGroup.jsx');
var ChartSelect = require('./ChartSelect.jsx');
var ChartBuilderStore = require("stores/ChartBuilderStore");
var ChartBuilderActions = require('actions/ChartBuilderActions');
var Chart = require('component/Chart.jsx');

module.exports = React.createClass({
    mixins: [Reflux.connect(ChartBuilderStore,"store")],
    _updateTitle: function(e){
      ChartBuilderActions.updateTitle(e.target.value);
    },
    _updateDescription: function(e){
      ChartBuilderActions.updateDescription(e.target.value);
    },
	render: function(){
	   var chart = <Chart type="LineChart" data={this.state.store.chartData} id="custom-chart" options={this.state.store.chartOptions} />;
	   
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
                       <RadioGroup name="show" value={this.state.store.regionRadioValue} values={this.state.store.regionRadios} onChange={ChartBuilderActions.selectShowRegionRadio} />
	              </div> 
	              <div className="right-page">
	              	<ChartSelect charts={this.state.store.chartTypes} value={this.state.store.selectedChart} onChange={ChartBuilderActions.selectChart} />
	              	<div className="chart-container">
	              	<div className="titleDiv">Group By</div>
	              	<RadioGroup name="groupby" value={this.state.store.groupByRadioValue} values={this.state.store.groupByRadios} onChange={ChartBuilderActions.selectGroupByRadio} />
	              	<Menu items={this.state.store.campaignList}
	              		      sendValue={ChartBuilderActions.addCampaignSelection}
	              		      searchable={true}>
	              				<span className="menu-span"> {this.state.store.campaignSelected.slug?this.state.store.campaignSelected.slug:"select campaign"} </span>
	              		</Menu>
	              	<Menu items={this.state.store.regionList}
	              		      sendValue={ChartBuilderActions.addRegionSelection}
	              		      searchable={true}>
	              				<span className="menu-span"> {this.state.store.regionSelected.title ? this.state.store.regionSelected.title:"select region"} </span>
	              		</Menu>
	              	{this.state.store.chartData.length?chart:null}
				    </div>
	              </div>
	            </div>
	            </form>
	           );
	}
});