'use strict';

var _      = require('lodash');
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

function findMatches(item, re) {
  var matches = [];

  if (re.test(_.get(item, 'title'))) {
    matches.push(item);
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    matches = matches.concat(findMatches(item.children, re));
  }

  return matches;
};

function filterMenu(items, pattern) {
  if (_.size(pattern) < 3) {
    return items;
  }

  var filtered = [];
  var re = new RegExp(pattern, 'gi');

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

  _updateFilter : function (filterFor, pattern) {
    var state = {};

    state[filterFor + 'Filter'] = pattern;

    this.setState(state);
  },

  setFilter : function (filterFor, pattern) {
    var state = {};
    state[filterFor + 'Filter'] = pattern;

    this.setState(state);
  },

	render: function(){
	   var chart = <Chart type="LineChart" data={this.state.store.chartData} id="custom-chart" options={this.state.store.chartOptions} />;

	   var campaignSelection = !!this.state.store.campaignSelected ?
      this.state.store.campaignSelected.slug :
      'Select Campaign';

     var campaigns = MenuItem.fromArray(
      filterMenu(this.state.store.campaignList, this.state.campaignFilter),
      ChartBuilderActions.addCampaignSelection);

     var indicators = MenuItem.fromArray(
      filterMenu(this.state.store.indicatorList, this.state.indicatorFilter),
      ChartBuilderActions.addIndicatorSelection);

     var regionSelection = !!this.state.store.regionSelected ?
      this.state.store.regionSelected.title :
      'Select Region';

     var regions = MenuItem.fromArray(
      filterMenu(this.state.store.regionList, this.state.regionFilter),
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
                      onSearch={_.partial(this.setFilter, 'indicator')}>
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
                    onSearch={_.partial(this.setFilter, 'campaign')}>
	              	  {campaigns}
              		</ButtonMenu>

	              	<ButtonMenu
                    icon='fa-globe'
                    text={regionSelection}
          		      searchable={true}
                    onSearch={_.partial(this.setFilter, 'region')}>
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
