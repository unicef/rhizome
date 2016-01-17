import React from 'react'
import Reflux from 'reflux'
// import _ from 'lodash'
// import moment from 'moment'

// import ChartWizardStep from './ChartWizardStep.jsx'
// import ChartWizardStepList from './ChartWizardStepList.jsx'
import DateRangePicker from 'component/DateTimePicker.jsx'
import LocationDropdownMenu from 'component/LocationDropdownMenu.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import ChartSelect from './ChartSelect.jsx'
import List from 'component/list/List.jsx'
// import MenuItem from 'component/MenuItem.jsx'
// import DropdownMenu from 'component/DropdownMenu.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
// import CampaignDropdownMenu from 'component/CampaignDropdownMenu.jsx'

import Chart from 'component/Chart.jsx'
// import RadioGroup from 'component/radio-group/RadioGroup.jsx'

import ExplorerStore from 'stores/ExplorerStore'
import ExplorerActions from 'actions/ExplorerActions'
import ChartWizardActions from 'actions/ChartWizardActions'
import ChartWizardStore from 'stores/ChartWizardStore'
// import options from './options/options'
// import previews from './preview/previews'

const defaultChartDef = {
  title: '',
  type: 'LineChart',
  indicators: [],
  countries: [],
  groupBy: 'indicator',
  timeRange: null,
  x: 0,
  xFormat: ',.0f',
  y: 0,
  yFormat: ',.0f',
  z: 0
}

// function filterMenu (items, pattern) {
//   if (!pattern || pattern.length < 3) {
//     return items
//   }
//
//   let match = _.partial(findMatches, _, new RegExp(pattern, 'gi'))
//
//   return _(items).map(match).flatten().value()
// }

// function findMatches (item, re) {
//   let matches = []
//
//   if (re.test(_.get(item, 'title'))) {
//     matches.push(_.assign({}, item, {filtered: true}))
//   }
//
//   if (!_.isEmpty(_.get(item, 'children'))) {
//     _.each(item.children, function (child) {
//       matches = matches.concat(findMatches(child, re))
//     })
//   }
//
//   return matches
// }

let ChartWizard = React.createClass({
  propTypes: {
    chartDef: React.PropTypes.object,
    save: React.PropTypes.func,
    cancel: React.PropTypes.func
  },

  mixins: [Reflux.connect(ChartWizardStore, 'data'), Reflux.connect(ExplorerStore)],

  getInitialState () {
    return {
      refer: 'first-indicator',
      startTime: '2016-01-01',
      endDate: '2016-30-01'
    }
  },

  componentWillMount: function () {
    ExplorerActions.getLocations()
    ExplorerActions.getIndicators()
  },

  componentDidMount () {
    this.chartDef = this.props.chartDef || defaultChartDef
    ChartWizardActions.initialize(this.chartDef)
  },

  componentWillReceiveProps () {
    ChartWizardActions.clear()
  },

  saveChart () {
    ChartWizardActions.saveChart(this.props.save)
  },

  toggleStep (refer) {
    return () => {
      this.setState({
        refer: refer
      })
    }
  },

  setLocationSearch (pattern) {
    this.setState({
      locationSearch: pattern
    })
  },

  render () {
    console.log('this dot state dot data: ', this.state.data)
    let locationStep = (
      <div>
        <LocationDropdownMenu
          text='Add Locations'
          locations={this.state.data.locationFilteredList}
          sendValue={ChartWizardActions.addLocation}
          style='databrowser__button' />
        <List items={this.state.data.location} removeItem={ChartWizardActions.removeLocation} />
        <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
      </div>
    )
    let indicatorStep = (
      <div>
        <IndicatorDropdownMenu
          indicators={this.state.data.indicatorList}
          text='Choose Indicators'
          sendValue={ChartWizardActions.addIndicator}
          style='databrowser__button' />
        <List items={this.state.data.indicatorSelected} removeItem={ChartWizardActions.removeIndicator} />
      </div>
    )
    let timePeriodStep = (
      <div>
        <DateRangePicker
          start={this.state.startTime}
          end={this.state.endTime}
          sendValue={ExplorerActions.updateDateRangePicker}
        />
    </div>
    )
    let chartTypeStep = (
      <label>
        <br></br>
        <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
          onChange={ChartWizardActions.changeChart}/>
      </label>
    )
    // locations={this.state.locations}
    // <List items={this.state.locationSelected} removeItem={ExplorerActions.removeLocation} />

    // <List items={this.state.indicatorSelected} removeItem={ExplorerActions.removeIndicator} />

    // let loadDataStep = (
    //   <a role='button'
    //      onClick={this.refresh}
    //      className={this.state.couldLoad ? 'button success' : 'button success disabled'}
    //      style={{marginTop: '21px'}} >
    //     <i className='fa fa-fw fa-refresh' />&emsp;Load Data
    //   </a>
    // )

    if (!this.state.data.chartDef.type) {
      return null
    }

    // let firstIndicatorStep = (
    //   <div>
    //     <p className='chart-wizard__para'>
    //       Please choose the first indicator you would like to show in the chart. You may also choose more indicators later.
    //     </p>
    //     <IndicatorDropdownMenu
    //       text={this.state.data.indicatorSelected[0] && this.state.data.indicatorSelected[0].name || ' Select an Indicator'}
    //       icon='fa-plus'
    //       indicators= {this.state.data.indicatorList}
    //       sendValue={ChartWizardActions.addFirstIndicator} />
    //     <span className='chart-wizard__next' onClick={this.toggleStep('location')}>Next</span>
    //   </div>
    // )

    // let locations = MenuItem.fromArray(filterMenu(this.state.data.locationFilteredList, this.state.locationSearch), ChartWizardActions.addLocation)
    // let locationStep = (
    //   <div>
    //     <DropdownMenu
    //       icon='fa-globe'
    //       text='Select Location'
    //       searchable
    //       onSearch={this.setLocationSearch}>
    //       {locations}
    //     </DropdownMenu>
    //     <List items={this.state.data.location} removeItem={ChartWizardActions.removeLocation} />
    //     <span className='chart-wizard__next' onClick={this.toggleStep('chart-type')}>Next</span>
    //   </div>
    // )

    // let chartTypeStep = (
    //   <div>
    //     <p className='chart-wizard__para'>What would the new chart look like?</p>
    //     <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
    //       onChange={ChartWizardActions.changeChart}/>
    //     <span className='chart-wizard__next' onClick={this.toggleStep('time-range')}>Next</span>
    //   </div>
    // )

    // let campaignListAsDate = _(this.state.data.campaignFilteredList).map(campaign => {
    //   return _.assign({}, campaign, {
    //     slug: moment(campaign.start_date).format('MMMM YYYY')
    //   })
    // }).uniq(_.property('slug')).value()

    // let timeRangeStep = (
    //   <div>
    //     <p className='chart-wizard__para'>Which time period would you like to display the data for?</p>
    //     <h4>Ending Time: </h4>
    //     <CampaignDropdownMenu
    //       text={this.state.data.campaign && moment(this.state.data.campaign.start_date).format('MMMM YYYY') || 'Select Ending Time'}
    //       campaigns={campaignListAsDate}
    //       sendValue={ChartWizardActions.addCampaign} />
    //     <RadioGroup name='time' title='Time Range'
    //       value={this.state.data.timeValue}
    //       values={this.state.data.timeRangeFilteredList} onChange={ChartWizardActions.changeTimeRadio} />
    //     <span className='chart-wizard__next' onClick={this.toggleStep('option')}>Next</span>
    //   </div>
    // )

    // let option = React.createElement(options[this.state.data.chartDef.type], {
    //   indicatorList: this.state.data.indicatorList,
    //   rawIndicators: this.state.data.rawIndicators,
    //   rawTags: this.state.data.rawTags,
    //   indicatorSelected: this.state.data.indicatorSelected,
    //   groupByValue: this.state.data.groupByValue,
    //   locationLevelValue: this.state.data.locationLevelValue,
    //   xFormatValue: this.state.data.xFormatValue,
    //   yFormatValue: this.state.data.yFormatValue
    // })

    // let optionStep = (
    //   <div>
    //     {option}
    //     <span className='chart-wizard__next' onClick={this.toggleStep('preview')}>Next</span>
    //   </div>
    // )

    // let preview = React.createElement(previews[this.state.data.chartDef.type], {
    //   chartTitle: this.state.data.chartDef.title,
    //   onEditTitle: ChartWizardActions.editTitle,
    //   palette: this.state.data.chartDef.palette,
    //   onChangePalette: ChartWizardActions.changePalette,
    //   xLabel: this.state.data.chartDef.xLabel,
    //   yLabel: this.state.data.chartDef.yLabel,
    //   onSetXYAxisLabel: ChartWizardActions.setXYAxisLabel
    // })

    // let previewStep = (
    //   <div>
    //     {preview}
    //      <span className='chart-wizard__save' onClick={this.saveChart}>
    //       {this.props.chartDef ? 'Update Chart' : 'Create Chart'}
    //     </span>
    //   </div>
    // )

    let chart = (
      <Chart id='custom-chart' type={this.state.data.chartDef.type} data={this.state.data.chartData}
        options={this.state.data.chartOptions}/>
    )

    // let locationName = this.state.data.location.map(location => location.name).join(', ')
    // let chartWizardSelector = <ChartWizardStepList onToggle={this.toggleStep} active={this.state.refer}>
    //     <ChartWizardStep
    //       title={`1. Select First Indicator${this.state.data.indicatorSelected[0] ? ' - ' + this.state.data.indicatorSelected[0].name : ''}`}
    //       refer='first-indicator'>
    //       {firstIndicatorStep}
    //     </ChartWizardStep>
    //     <ChartWizardStep title={`2. Select Location${locationName.length > 0 ? ' - ' + locationName : ''}`}
    //       refer='location'>
    //       {locationStep}
    //     </ChartWizardStep>
    //     <ChartWizardStep
    //       title={`3. Select Chart Type${this.state.data.chartDef.type ? ' - ' + this.state.data.chartDef.type.match(/[A-Z][a-z]*/g).join(' ') : ''}`}
    //       refer='chart-type'>
    //       {chartTypeStep}
    //     </ChartWizardStep>
    //     <ChartWizardStep
    //       title={`4. Select Time Range${this.state.data.campaign ? ' - ' + moment(this.state.data.campaign.start_date).format('MMMM YYYY') : ''}`}
    //       refer='time-range'>
    //       {timeRangeStep}
    //     </ChartWizardStep>
    //     <ChartWizardStep title='5. Customise Options' refer='option'>
    //       {optionStep}
    //     </ChartWizardStep>
    //     <ChartWizardStep title='6. Preview' refer='preview'>
    //       {previewStep}
    //     </ChartWizardStep>
    //   </ChartWizardStepList>

    let chartWizardSelector = <div className='medium-3 columns'>
          <h1>Chart Builder</h1>
            <from className='inline'>
              {locationStep}
              {indicatorStep}
              {timePeriodStep}
              {chartTypeStep}
            </from>
          </div>

    return (
      <div className='chart-wizard'>
        {chartWizardSelector}
        <PreviewScreen isLoading={this.state.data.isLoading}>
          {this.state.data.canDisplayChart
            ? chart
            : (<div className='empty'>No Data</div>)
          }
        </PreviewScreen>
      </div>
    )
  }
})
// <span className='chart-wizard__cancel' onClick={this.props.cancel}>Cancel</span>

export default ChartWizard
