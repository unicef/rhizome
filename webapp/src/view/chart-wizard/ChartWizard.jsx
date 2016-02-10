import React from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import ExpandableSection from 'component/ExpandableSection.jsx'
import DateRangePicker from 'component/DateRangePicker.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import ChartSelect from './ChartSelect.jsx'

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

  previewData: function (data) {
    console.log(data)
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
    return (
      <div className='chart-wizard'>
        <div className='medium-3 columns'>
          <h1>Chart Builder</h1>
          <div className='row'>
            <div className='medium-6 columns'>
              <ExpandableSection title='Indicators' refer='preview'>
                <DropdownMenu
                  items={availableIndicators}
                  sendValue={ChartWizardActions.addIndicator}
                  item_plural_name='Indicators'
                  text='Choose Indicators'
                  style='databrowser__button'/>
                <ReorderableList items={this.state.data.indicatorSelected} removeItem={ChartWizardActions.removeIndicator} dragItem={ChartWizardActions.reorderIndicator} />
              </ExpandableSection>
            </div>
            <div className='medium-6 columns'>
              <ExpandableSection title='Locations' refer='preview'>
                 <DropdownMenu
                  items={location_options}
                  sendValue={ChartWizardActions.addLocation}
                  item_plural_name='Locations'
                  text='Choose Locations'
                  style='databrowser__button'
                  icon='fa-globe'
                  grouped/>
                <List items={this.state.data.selected_locations} removeItem={ChartWizardActions.removeLocation} />
                <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
              </ExpandableSection>
            </div>
          </div>
          <ExpandableSection title='Time' refer='preview'>
            <DateRangePicker
              sendValue={ChartWizardActions.updateDateRangePicker}
              start={startDate}
              end={endDate}
              fromComponent='ChartWizard' />
          </ExpandableSection>

          <ExpandableSection title='Chart Type' refer='preview'>
            <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
              onChange={ChartWizardActions.changeChart}/>
          </ExpandableSection>

          <div className='row'>
            <button className='chart-wizard__save' onClick={this.saveChart}>
                Save
            </button>
            <button className='chart-wizard__cancel' onClick={this.props.cancel}>
                Cancel
            </button>
          </div>

          <SimplePreview
            chartTitle={this.props.chartDef.title}
            onEditTitle={ChartWizardActions.editTitle}
            palette={palette}
            onChangePalette={ChartWizardActions.changePalette} />
        </div>
        <PreviewScreen isLoading={this.state.data.isLoading}>
          {this.state.data.canDisplayChart ? chart : (<div className='empty'>No Data</div>) }
        </PreviewScreen>
        <div className='row'></div>
      </div>
    )
  }
})

export default ChartWizard
