'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');
var moment = require('moment');

var DropdownMenu         = require('component/DropdownMenu.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');
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
  componentDidMount:function(){
     ChartBuilderActions.initialize(this.props.chartDef);
  },
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
  _updateXAxis : function(e){
     ChartBuilderActions.selectXAxis(parseInt(e.target.value));
  },
  _updateYAxis : function(e){
     ChartBuilderActions.selectYAxis(parseInt(e.target.value));
  },
  setFilter : function (filterFor, pattern) {
    var state = {};
    state[filterFor + 'Filter'] = pattern;

    this.setState(state);
  },
  createChart:function(){
    this.props.callback(this.state.store.chartDefinition());
  },

	render: function(){
	   console.log(this.props.chartDef);
	   var chart = <Chart type={this.state.store.chartTypes[this.state.store.selectedChart].name} data={this.state.store.chartData} id="custom-chart" options={this.state.store.chartOptions} />;
	   var canDisplayChartReason = (<div>{this.state.store.canDisplayChartReason()}</div>);
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
      
     var axisOptions = this.state.store.indicatorsSelected.map(function(indicator,index){
       return <option key={indicator.id} value={index}>{indicator.name}</option>;
     });
     
     /*  <div className="titleDiv" onChange={this._updateDescription}>Description</div>
      <textarea value={this.state.store.description} onChange={this._updateDescription}></textarea> */
     
     var leftPage = (<div className="left-page">
     	                   <div className="titleDiv">Title</div>
     	                   <input type="text" value={this.state.store.title} onChange={this._updateTitle}/>

     	                   <div className="titleDiv">Indicators</div>

                         <IndicatorDropdownMenu
                           text='Add Indicators'
                           icon='fa-plus'
                           indicators={this.state.store.indicatorList}
                           sendValue={ChartBuilderActions.addIndicatorSelection}>
                         </IndicatorDropdownMenu>
     
     		             <List items={this.state.store.indicatorsSelected} removeItem={ChartBuilderActions.removeIndicatorSelection} />
    
                      <a href="#" className="button" onClick={this.createChart}>{this.props.chartDef?"Update Chart":"Create Chart"}</a>
                      <a href="#" onClick={this.props.cancel}>Cancel without saving chart</a>

     	              </div>);
     var groupBy = 	(<div className="grouping">
        	<div className="titleDiv">Group By</div>
        	<RadioGroup name="groupby" horizontal={true}  value={this.state.store.groupByRadioValue} values={this.state.store.groupByRadios} onChange={ChartBuilderActions.selectGroupByRadio} />
        	</div>);  
     var chooseAxis = (<div className="grouping">
		     	<div>x axis: <select onChange={this._updateXAxis}>{axisOptions}</select></div>
		     	<div>y axis: <select onChange={this._updateYAxis}>{axisOptions}</select></div>
		     </div>);           
     var rightPage = (<div className="right-page">
     	              	<ChartSelect charts={this.state.store.chartTypes} value={this.state.store.selectedChart} onChange={ChartBuilderActions.selectChart} />
     	              	<div className="chart-options-container">
     	              	{this.state.store.chartTypes[this.state.store.selectedChart].groupBy?groupBy:null}
     	              	<div className="grouping">
     	                   <div className="titleDiv">Show</div>
     	                   <RadioGroup name="show" horizontal={true}  value={this.state.store.regionRadioValue} values={this.state.store.regionRadios} onChange={ChartBuilderActions.selectShowRegionRadio} />
                        </div>
                        <div className="grouping">
                        		<div className="titleDiv">Time Span</div>
                    			<RadioGroup name="time" horizontal={true} value={this.state.store.timeRadioValue} values={this.state.store.timeRadios()} onChange={ChartBuilderActions.selectTimeRadio} />
                    	</div>
                    	{this.state.store.chartTypes[this.state.store.selectedChart].chooseAxis?chooseAxis:null}
     					</div>
     					<div className="chart-container">
                <div className="grouping">
                  <div className="titleDiv">Preview</div>
                  <div className="preview-section">
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
                       {this.state.store.canDisplayChart()?chart:canDisplayChartReason}
         				    </div>
                  </div>
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
