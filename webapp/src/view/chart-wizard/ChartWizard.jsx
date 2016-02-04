import React from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import ChartWizardStep from './ChartWizardStep.jsx'
import DateRangePicker from 'component/DateTimePicker.jsx'
import LocationDropdownMenu from 'component/LocationDropdownMenu.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import ChartSelect from './ChartSelect.jsx'
import List from 'component/list/List.jsx'
import ReorderableList from 'component/list/ReorderableList.jsx'

import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import Chart from 'component/Chart.jsx'

import ExplorerStore from 'stores/ExplorerStore'
import ExplorerActions from 'actions/ExplorerActions'
import ChartWizardActions from 'actions/ChartWizardActions'
import ChartWizardStore from 'stores/ChartWizardStore'
// import options from './options/options'
import previews from './preview/previews'

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

let ChartWizard = React.createClass({
  propTypes: {
    chartDef: React.PropTypes.object,
    save: React.PropTypes.func,
    cancel: React.PropTypes.func
  },

  mixins: [Reflux.connect(ChartWizardStore, 'data'), Reflux.connect(ExplorerStore)],

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
    // console.log('this.state: ', this.state)
    // console.log('this.props: ', this.props)

    let availableIndicators = this.state.data.indicatorList
    let indicatorStep = (
      <div>
        <ChartWizardStep title='Indicators' refer='preview'>
        <IndicatorDropdownMenu
          indicators={availableIndicators}
          text='Choose Indicators'
          sendValue={ChartWizardActions.addIndicator}
          style='databrowser__button' />
        <ReorderableList items={this.state.data.indicatorSelected} removeItem={ChartWizardActions.removeIndicator} dragItem={ChartWizardActions.reorderIndicator} />
        </ChartWizardStep>
      </div>
    )

    let locationStep = (
      <div>
        <ChartWizardStep title='Locations' refer='preview'>
        <LocationDropdownMenu
          text='Add Locations'
          locations={this.state.data.locationFilteredList}
          sendValue={ChartWizardActions.addLocation}
          style='databrowser__button' />
        <List items={this.state.data.location} removeItem={ChartWizardActions.removeLocation} />
        <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
        </ChartWizardStep>
      </div>
    )
    let timePeriodStep = (
      <div>
        <ChartWizardStep title='Time' refer='preview'>
        <DateRangePicker
          start={moment(this.state.data.chartDef.startDate).toDate()}
          end={moment(this.state.data.chartDef.endDate).toDate()}
          sendValue={ChartWizardActions.updateDateRangePicker}
        />
        </ChartWizardStep>
    </div>
    )
    let chartTypeStep = (
      <div>
        <ChartWizardStep title='Chart Type' refer='preview'>
        <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
          onChange={ChartWizardActions.changeChart}/>
        </ChartWizardStep>
      </div>
    )

    if (!this.state.data.chartDef.type) {
      return null
    }

    let styleSelector = React.createElement(previews[this.state.data.chartDef.type], {
      chartTitle: this.state.data.chartDef.title,
      onEditTitle: ChartWizardActions.editTitle,
      palette: this.state.data.chartDef.palette,
      onChangePalette: ChartWizardActions.changePalette,
      xLabel: this.state.data.chartDef.xLabel,
      yLabel: this.state.data.chartDef.yLabel,
      onSetXYAxisLabel: ChartWizardActions.setXYAxisLabel
    })

    let chart = (
      <Chart id='custom-chart' type={this.state.data.chartDef.type} data={this.state.data.chartData}
        options={this.state.data.chartOptions}/>
    )
    let chartWizardSelector = <div className='medium-3 columns'>
          <h1>Chart Builder</h1>
            {indicatorStep}
            {locationStep}
            {timePeriodStep}
            {chartTypeStep}
            {styleSelector}
            <div className='row'>
              <button className='chart-wizard__save' onClick={this.saveChart}>
                  Save
              </button>
              <button className='chart-wizard__cancel' onClick={this.props.cancel}>
                  Cancel
              </button>
           </div>
          </div>

    let chartWizardEditor = <div className='row'>
        <div className='medium-4 columns'>A</div>
        <div className='medium-4 columns'>B</div>
        <div className='medium-4 columns'>C</div>
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
        {chartWizardEditor}
      </div>
    )
  }
})

export default ChartWizard
