'use strict'

var _ = require('lodash')
var React = require('react')
var Reflux = require('reflux')
var moment = require('moment')

var DropdownMenu = require('component/DropdownMenu.jsx')
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx')
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx')
var Chart = require('component/Chart.jsx')
var ChartBuilderActions = require('actions/ChartBuilderActions')
var ChartBuilderStore = require('stores/ChartBuilderStore')
var ChartSelect = require('./ChartSelect.jsx')
var List = require('component/list/List.jsx')
var MenuItem = require('component/MenuItem.jsx')
var RadioGroup = require('component/radio-group/RadioGroup.jsx')
var TitleInput = require('component/TitleInput.jsx')

function findMatches (item, re) {
  var matches = []

  if (re.test(_.get(item, 'title'))) {
    matches.push(_.assign({}, item, {filtered: true}))
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    _.each(item.children, function (child) {
      matches = matches.concat(findMatches(child, re))
    })
  }

  return matches
}

function filterMenu (items, pattern) {
  if (_.size(pattern) < 3) {
    return items
  }

  var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'))

  return _(items).map(match).flatten().value()
}

function campaignDisplayFormat (campaign) {
  return moment(campaign.start_date).format('MMMM YYYY')
}

module.exports = React.createClass({
  propTypes: {
    chartDef: React.PropTypes.object,
    // location: React.PropTypes.string,
    // callback: React.PropTypes.function,
    // cancel: React.PropTypes.function,
    // children: React.PropTypes.array,
  },
  mixins: [Reflux.connect(ChartBuilderStore, 'store')],
  getInitialState: function () {
    return {
      title: ''
    }
  },
  componentDidMount: function () {
    ChartBuilderActions.initialize(
        this.props.chartDef,
        this.props.location,
        this.props.campaign
      )
    this.props.chartDef && this.setState({title: this.props.chartDef.title})
  },
  _updateTitle: function (newText) {
    // this.setState({title:e.currentTarget.value})

    // clearTimeout(this.timer)
    // this.timer = setTimeout(function (){
    ChartBuilderActions.updateTitle(newText)
    // }.bind(this), 1000)
  },

  _updateDescription: function (e) {
    ChartBuilderActions.updateDescription(e.target.value)
  },

  _updateFilter: function (filterFor, pattern) {
    var state = {}

    state[filterFor + 'Filter'] = pattern

    this.setState(state)
  },
  _updateXAxis: function (e) {
    ChartBuilderActions.selectXAxis(parseInt(e.target.value, 10))
  },
  _updateYAxis: function (e) {
    ChartBuilderActions.selectYAxis(parseInt(e.target.value, 10))
  },
  setFilter: function (filterFor, pattern) {
    var state = {}
    state[filterFor + 'Filter'] = pattern

    this.setState(state)
  },
  createChart: function () {
    this.props.callback(this.state.store.chartDefinition())
  },

  render: function () {
    var chart = <Chart type={this.state.store.chartTypes[this.state.store.selectedChart].name}
                   data={this.state.store.chartData} id='custom-chart' options={this.state.store.chartOptions}/>
    var canDisplayChartReason = (<div>{this.state.store.canDisplayChartReason()}</div>)
    var loadingDiv = (<div className='loading-div'><i className='fa fa-spinner fa-spin fa-5x'></i></div>)

    var campaignSelection = this.state.store.campaignSelected
      ? campaignDisplayFormat(this.state.store.campaignSelected)
      : 'Select Campaign'

    var locationSelection = this.state.store.locationSelected
      ? this.state.store.locationSelected.name
      : 'Select location'

    var locations = MenuItem.fromArray(
      filterMenu(this.state.store.locationList, this.state.locationFilter),
      ChartBuilderActions.addLocationSelection)

    var axisOptions = this.state.store.indicatorsSelected.map(function (indicator, index) {
      return <option key={indicator.id} value={index}>{indicator.name}</option>
    })

    /*  <div className='titleDiv' onChange={this._updateDescription}>Description</div>
     <textarea value={this.state.store.description} onChange={this._updateDescription}></textarea> */

    var leftPage = (<div className='left-page'>
      <div className='titleDiv'>Title</div>
      <TitleInput class='descriptionField' initialText={this.state.title} save={this._updateTitle}/>

      <div className='titleDiv'>Indicators</div>

      <IndicatorDropdownMenu
        text='Add Indicators'
        icon='fa-plus'
        indicators={this.state.store.indicatorList}
        sendValue={ChartBuilderActions.addIndicatorSelection} />

      <List items={this.state.store.indicatorsSelected} removeItem={ChartBuilderActions.removeIndicatorSelection}/>

      <a href='#' className='button success'
         onClick={this.createChart}>{this.props.chartDef ? 'Update Chart' : 'Create Chart'}</a>
      <a href='#' onClick={this.props.cancel}>Cancel without saving chart</a>

    </div>)
    var groupBy = (<div className='grouping'>
      <div className='titleDiv'>Group By</div>
      <RadioGroup name='groupby' horizontal value={this.state.store.groupByRadioValue}
                  values={this.state.store.groupByRadios} onChange={ChartBuilderActions.selectGroupByRadio}/>
    </div>)
    var chooseAxis = (<div className='grouping'>
      <div>
        <div className='titleDiv'>X Axis</div>
        <select className='medium-6' onChange={this._updateXAxis}>{axisOptions}</select></div>
      <div>
        <div className='titleDiv'>Y Axis</div>
        <select className='medium-6' onChange={this._updateYAxis}>{axisOptions}</select></div>
    </div>)
    var formatXAxis = (
      <div className='grouping'>
        <div className='titleDiv'>X Format</div>
        <RadioGroup name='xFormat' horizontal value={this.state.store.xFormatRadioValue}
                    values={this.state.store.formatRadios()} onChange={ChartBuilderActions.selectXFormatRadio}/>
      </div>
    )
    var rightPage = (<div className='right-page'>
        <ChartSelect charts={this.state.store.chartTypes} value={this.state.store.selectedChart}
                     onChange={ChartBuilderActions.selectChart}/>

        <div className='chart-options-container'>
          {this.state.store.chartTypes[this.state.store.selectedChart].groupBy ? groupBy : null}
          <div className='grouping'>
            <div className='titleDiv'>Show</div>
            <RadioGroup name='show' horizontal value={this.state.store.locationRadioValue}
                        values={this.state.store.locationRadios} onChange={ChartBuilderActions.selectShowLocationRadio}/>
          </div>
          <div className='grouping'>
            <div className='titleDiv'>Time Span</div>
            <RadioGroup name='time' horizontal value={this.state.store.timeRadioValue}
                        values={this.state.store.timeRadios()} onChange={ChartBuilderActions.selectTimeRadio}/>
          </div>
          {this.state.store.chartTypes[this.state.store.selectedChart].chooseAxis ? formatXAxis : null}
          <div className='grouping'>
            <div className='titleDiv'>
              {this.state.store.chartTypes[this.state.store.selectedChart].chooseAxis ? 'Y ' : null}Format
            </div>
            <RadioGroup name='format' horizontal value={this.state.store.formatRadioValue}
                        values={this.state.store.formatRadios()} onChange={ChartBuilderActions.selectFormatRadio}/>
          </div>
          {this.state.store.chartTypes[this.state.store.selectedChart].chooseAxis ? chooseAxis : null}
        </div>
        <div className='chart-container'>
          <div className='grouping'>
            <div className='titleDiv'>Preview</div>
            <div className='preview-section'>
              <div className='dropdown-wrapper'>
                <CampaignDropdownMenu
                  text={campaignSelection}
                  campaigns={this.state.store.campaignList}
                  sendValue={ChartBuilderActions.addCampaignSelection} />
              </div>
              <div className='dropdown-wrapper'>
                <DropdownMenu
                  icon='fa-globe'
                  text={locationSelection}
                  searchable
                  onSearch={_.partial(this.setFilter, 'location')}>
                  {locations}
                </DropdownMenu>
              </div>
              {this.state.store.loading ? loadingDiv : null}
              {this.state.store.canDisplayChart() ? chart : canDisplayChartReason}
            </div>
          </div>
        </div>
      </div>
    )

    return (<form className='inline'>
        <div className='visualization-builder-container'>
          {leftPage}
          {rightPage}
        </div>
      </form>
    )
  }
})
