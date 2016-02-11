import React from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import ExpandableSection from 'component/ExpandableSection.jsx'
import DateRangePicker from 'component/DateRangePicker.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import ChartSelect from './ChartSelect.jsx'
import PalettePicker from './preview/PalettePicker.jsx'

import TitleInput from 'component/TitleInput.jsx'
import List from 'component/list/List.jsx'
import ReorderableList from 'component/list/ReorderableList.jsx'
import DropdownMenu from 'component/menus/DropdownMenu.jsx'
import Chart from 'component/Chart.jsx'

import ChartWizardActions from 'actions/ChartWizardActions'
import ChartWizardStore from 'stores/ChartWizardStore'
import SimplePreview from './preview/SimplePreview.jsx'

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

  mixins: [Reflux.connect(ChartWizardStore, 'data')],

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

  setLocationSearch: function (pattern) {
    this.setState({
      locationSearch: pattern
    })
  },

  render: function () {
    let availableIndicators = this.state.data.indicatorList
    let palette = this.state.data.chartDef.palette || 'orange'
    let startDate = moment()
    let endDate = moment()

    if (this.state.data.chartDef) {
      startDate = moment(this.state.data.chartDef.startDate, 'YYYY-MM-DD').toDate()
      endDate = moment(this.state.data.chartDef.endDate, 'YYYY-MM-DD').toDate()
    }

    if (!this.state.data.chartDef.type) {
      return null
    }

    let chart = (
      <Chart id='custom-chart' type={this.state.data.chartDef.type} data={this.state.data.chartData}
        options={this.state.data.chartOptions}/>
    )

    let location_options = [
      { title: 'by Tag', value: this.state.data.location_tags },
      { title: 'by Country', value: this.state.data.locationFilteredList }
    ]

    let clear_locations_button = '';
    if (this.state.data.selected_locations.length > 3 ) {
      clear_locations_button = <a className='remove-filters-link' onClick={ChartWizardActions.clearSelectedLocations}>Remove All </a>
    }

    let clear_indicators_button = '';
    if (this.state.data.indicatorSelected.length > 3 ) {
      clear_indicators_button = <a className='remove-filters-link' onClick={ChartWizardActions.clearSelectedIndicators}>Remove All </a>
    }
    return (
      <section className='chart-wizard'>
        <h1 className='medium-12 columns text-center'>Chart Builder</h1>
        <div className='medium-1 columns'>
            <h3>Chart Type</h3>
            <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
              onChange={ChartWizardActions.changeChart}/>
            <br/>
            <h3>Color Scheme</h3>
            <PalettePicker value={palette} onChange={ChartWizardActions.changePalette}/>
        </div>
        <div className='medium-3 columns'>
          <div className='row'>
            <h3>Chart Title</h3>
            <TitleInput initialText={this.props.chartDef.title} save={ChartWizardActions.editTitle}/>
            <br/>
            <h3>Time</h3>
            <DateRangePicker
              sendValue={ChartWizardActions.updateDateRangePicker}
              start={startDate}
              end={endDate}
              fromComponent='ChartWizard' />
            <br/>
          </div>
          <div className='row data-filters'>
            <br/>
            <div className='medium-6 columns'>
                <h3 class="chart-wizard_section-heading">
                  Indicators
                  <DropdownMenu
                    items={availableIndicators}
                    sendValue={ChartWizardActions.addIndicator}
                    item_plural_name='Indicators'
                    style='icon-button right'
                    icon='fa-plus' />
                </h3>
                {clear_indicators_button}
                <ReorderableList items={this.state.data.indicatorSelected} removeItem={ChartWizardActions.removeIndicator} dragItem={ChartWizardActions.reorderIndicator} />
            </div>
            <div className='medium-6 columns'>
              <h3 class="chart-wizard_section-heading">
                Locations
                <DropdownMenu
                  items={location_options}
                  sendValue={ChartWizardActions.addLocation}
                  item_plural_name='Locations'
                  style='icon-button right'
                  icon='fa-plus'
                  grouped/>
              </h3>
              {clear_locations_button}
              <List items={this.state.data.selected_locations} removeItem={ChartWizardActions.removeLocation} />
              <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
            </div>
          </div>
        </div>
        <div className='medium-8 columns'>
          <PreviewScreen isLoading={this.state.data.isLoading}>
            {this.state.data.canDisplayChart ? chart : (<div className='empty'>No Data</div>) }
          </PreviewScreen>
          <div className='row'>
            <div className='medium-2 columns right'>
              <button className='right chart-wizard__save' onClick={this.saveChart}>
                  Save Chart
              </button>
            </div>
          </div>
        </div>
      </section>
    )
  }
})

export default ChartWizard
