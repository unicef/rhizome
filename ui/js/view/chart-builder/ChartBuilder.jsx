'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');
var moment = require('moment');

var DropdownMenu         = require('component/DropdownMenu.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');
var Chart                = require('component/Chart.jsx');
var ChartBuilderActions  = require('actions/ChartBuilderActions');
var ChartBuilderStore    = require("stores/ChartBuilderStore");
var ChartSelect          = require('./ChartSelect.jsx');
var List                 = require('component/list/List.jsx');
var MenuItem             = require('component/MenuItem.jsx');
var RadioGroup           = require('component/radio-group/RadioGroup.jsx');

function findMatches(item, re) {
  var matches = [];

  if (re.test(_.get(item, 'title'))) {
    matches.push(_.assign({}, item, { filtered : true }));
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    _.each(item.children, function (child) {
      matches = matches.concat(findMatches(child, re));
    })
  }

  return matches;
};

function filterMenu(items, pattern) {
  if (_.size(pattern) < 3) {
    return items;
  }

  var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'));

  return _(items).map(match).flatten().value();
}

function campaignDisplayFormat(campaign) {
  return moment(campaign.start_date).format('MMMM YYYY');
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
	   var chart = <Chart type={this.state.store.chartTypes[this.state.store.selectedChart].name} data={this.state.store.chartData} id="custom-chart" options={this.state.store.chartOptions} />;
	   var loadingDiv = (<div className="loading-div"><i className="fa fa-spinner fa-spin fa-5x"></i></div>);


	   var campaignSelection = !!this.state.store.campaignSelected ?
      campaignDisplayFormat(this.state.store.campaignSelected) :
      'Select Campaign';

     var indicators = MenuItem.fromArray(
      filterMenu(this.state.store.indicatorList, this.state.indicatorFilter),
      ChartBuilderActions.addIndicatorSelection);

     var regionSelection = !!this.state.store.regionSelected ?
      this.state.store.regionSelected.name :
      'Select Region';

     var regions = MenuItem.fromArray(
      filterMenu(this.state.store.regionList, this.state.regionFilter),
      ChartBuilderActions.addRegionSelection);

     var leftPage = (<div className="left-page">
     	                   <div className="titleDiv">Title</div>
     	                   <input type="text" value={this.state.store.title} onChange={this._updateTitle}/>
     	                   <div className="titleDiv" onChange={this._updateDescription}>Description</div>
     	                   <textarea value={this.state.store.description} onChange={this._updateDescription}></textarea>
     	                   <div className="titleDiv">Indicators</div>
     
                         <DropdownMenu text='Select Indicators'
                           searchable={true}
                           onSearch={_.partial(this.setFilter, 'indicator')}>
                           {indicators}
                         </DropdownMenu>
     
     		               <List items={this.state.store.indicatorsSelected} removeItem={ChartBuilderActions.removeIndicatorSelection} />
     
     	              </div>);
     var rightPage = (<div className="right-page">
     	              	<ChartSelect charts={this.state.store.chartTypes} value={this.state.store.selectedChart} onChange={ChartBuilderActions.selectChart} />
     	              	<div className="chart-options-container">
     	              	<div className="grouping">
     		              	<div className="titleDiv">Group By</div>
     		              	<RadioGroup name="groupby" value={this.state.store.groupByRadioValue} values={this.state.store.groupByRadios} onChange={ChartBuilderActions.selectGroupByRadio} />
     		              	</div>
     	              	<div className="grouping">
     	                   <div className="titleDiv">Show</div>
     	                   <RadioGroup name="show" value={this.state.store.regionRadioValue} values={this.state.store.regionRadios} onChange={ChartBuilderActions.selectShowRegionRadio} />
                        </div>
                        <div className="grouping">
                        		<div className="titleDiv">Time Span</div>
                    			<RadioGroup name="time" horizontal={true} value={this.state.store.timeRadioValue} values={this.state.store.timeRadios()} onChange={ChartBuilderActions.selectTimeRadio} />
                    		</div>
     					</div>
     					<div className="chart-container">
     					<div className="dropdown-wrapper">
                       <CampaignDropdownMenu
                         text={campaignSelection}
                         campaigns={this.state.store.campaignList}
                         sendValue={ChartBuilderActions.addCampaignSelection}>
                       </CampaignDropdownMenu>
                        </div>
      					<div className="dropdown-wrapper">
     	              	<DropdownMenu
                         icon='fa-globe'
                         text={regionSelection}
               		      searchable={true}
                         onSearch={_.partial(this.setFilter, 'region')}>
                         {regions}
                   		</DropdownMenu>
						</div>
                       {this.state.store.loading?loadingDiv:null}
                       {this.state.store.canDisplayChart()?chart:null}
     				    </div>
     				    </div>
     	              );

	   return (<form className="inline">
	           <div className="visualization-builder-container">
				{leftPage}{rightPage}
				 </div>
	            </form>
	           );
	}
});
