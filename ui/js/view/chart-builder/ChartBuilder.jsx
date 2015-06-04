'use strict';

var React  = require('react');
var Reflux = require('reflux/src');

var ButtonMenu          = require('component/ButtonMenu.jsx');
var Chart               = require('component/Chart.jsx');
var ChartBuilderActions = require('actions/ChartBuilderActions');
var ChartBuilderStore   = require("stores/ChartBuilderStore");
var ChartSelect         = require('./ChartSelect.jsx');
var List                = require('component/list/List.jsx');
var MenuItem            = require('component/MenuItem.jsx');
var RadioGroup          = require('component/radio-group/RadioGroup.jsx');

function noop() {}

function findMatches(item, re) {
  var matches = [];

  if (re.test(item.title)) {
    matches.push(item);
  }

  if (item.children) {
    item.children.forEach(function (child) {
      matches = matches.concat(findMatches(child, re));
    });
  }

  return matches;
}

function filterMenu(items, pattern) {
  var filtered = [];
  var re = new RegEx(pattern, 'gi');

  _.each(items, function (item) {
    filtered = filtered.concat(findMatches(item, re));
  });

  return filtered;
}

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

	   var campaignSelection = !!this.state.store.campaignSelected ?
      this.state.store.campaignSelected.slug :
      'Select Campaign';

     var campaigns = MenuItem.fromArray(this.state.store.campaignList,
      ChartBuilderActions.addCampaignSelection);

     var indicators = MenuItem.fromArray(this.state.store.indicatorList,
      ChartBuilderActions.addIndicatorSelection);

     var regionSelection = !!this.state.store.regionSelected ?
      this.state.store.regionSelected.title :
      'Select Region';

     var regions = MenuItem.fromArray(this.state.store.regionList,
      ChartBuilderActions.addRegionSelection);

	   return (<form className="inline">
	           <div className="visualization-builder-container">
	              <div className="left-page">
	                   <div className="titleDiv">Title</div>
	                   <input type="text" value={this.state.store.title} onChange={this._updateTitle}/>
	                   <div className="titleDiv" onChange={this._updateDescription}>Description</div>
	                   <textarea value={this.state.store.description} onChange={this._updateDescription}></textarea>
	                   <div className="titleDiv">Indicators</div>

                    <ButtonMenu text='Select Indicators'
                      searchable={true}
                      onSearch={noop}>
                      {indicators}
                    </ButtonMenu>

		               <List items={this.state.store.indicatorsSelected} removeItem={ChartBuilderActions.removeIndicatorSelection} />
		               <div className="titleDiv">Show</div>
                       <RadioGroup name="show" value={this.state.store.regionRadioValue} values={this.state.store.regionRadios} onChange={ChartBuilderActions.selectShowRegionRadio} />
	              </div>

	              <div className="right-page">
	              	<ChartSelect charts={this.state.store.chartTypes} value={this.state.store.selectedChart} onChange={ChartBuilderActions.selectChart} />
	              	<div className="chart-container">
	              	<div className="titleDiv">Group By</div>
	              	<RadioGroup name="groupby" value={this.state.store.groupByRadioValue} values={this.state.store.groupByRadios} onChange={ChartBuilderActions.selectGroupByRadio} />

	              	<ButtonMenu
                    text={campaignSelection}
                    icon='fa-calendar'
          		      searchable={true}
                    onSearch={noop}>
	              	  {campaigns}
              		</ButtonMenu>

	              	<ButtonMenu
                    icon='fa-globe'
                    text={regionSelection}
          		      searchable={true}
                    onSearch={noop}>
                    {regions}
              		</ButtonMenu>

	              	{this.state.store.chartData.length?chart:null}
				    </div>
	              </div>
	            </div>
	            </form>
	           );
	}
});
