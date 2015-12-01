import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'

import ChartWizardStep from './ChartWizardStep.jsx'
import ChartWizardStepList from './ChartWizardStepList.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import ChartSelect from './ChartSelect.jsx'
import List from 'component/list/List.jsx'
import MenuItem from 'component/MenuItem.jsx'
import DropdownMenu from 'component/DropdownMenu.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import CampaignDropdownMenu from 'component/CampaignDropdownMenu.jsx'
import TitleInput from 'component/TitleInput.jsx'
import Chart from 'component/Chart.jsx'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'
import CheckBoxGroup from 'component/CheckBoxGroup.jsx'

import ChartWizardActions from 'actions/ChartWizardActions'
import ChartWizardStore from 'stores/ChartWizardStore'
import options from './options/options'

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

function filterMenu (items, pattern) {
  if (!pattern || pattern.length < 3) {
    return items
  }

  let match = _.partial(findMatches, _, new RegExp(pattern, 'gi'))

  return _(items).map(match).flatten().value()
}

function findMatches (item, re) {
  let matches = []

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

let ChartWizard = React.createClass({
  propTypes: {
    chartDef: React.PropTypes.object,
    save: React.PropTypes.func,
    cancel: React.PropTypes.func
  },

  mixins: [Reflux.connect(ChartWizardStore, 'data')],

  getInitialState () {
    return {
      refer: 'country'
    }
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
    if (!this.state.data.chartDef.type) {
      return null
    }

    let countryStep = (
      <div>
        <p className='chart-wizard__para'>Which country's data will the new chart visualise?</p>
        <div>
          <CheckBoxGroup name='country' title='Select Country'
            value={this.state.data.countrySelected.map(c => c.index)}
            values={this.state.data.countries}
            onChange={ChartWizardActions.changeCountry} />
        </div>
        <span className='chart-wizard__next' onClick={this.toggleStep('first-indicator')}>Next</span>
      </div>
    )

    let firstIndicatorStep = (
      <div>
        <p className='chart-wizard__para'>
          Please choose the first indicator you would like to show in the chart. You may also choose more indicators later.
        </p>
        <IndicatorDropdownMenu
          text={this.state.data.indicatorSelected[0] && this.state.data.indicatorSelected[0].name || 'Add Indicators'}
          icon='fa-plus'
          indicators= {this.state.data.indicatorList}
          sendValue={ChartWizardActions.addFirstIndicator} />
        <span className='chart-wizard__next' onClick={this.toggleStep('location')}>Next</span>
      </div>
    )

    let locations = MenuItem.fromArray(filterMenu(this.state.data.locationFilteredList, this.state.locationSearch), ChartWizardActions.addLocation)
    let locationStep = (
      <div>
        <DropdownMenu
          icon='fa-globe'
          text='Select Location'
          searchable
          onSearch={this.setLocationSearch}>
          {locations}
        </DropdownMenu>
        <List items={this.state.data.location} removeItem={ChartWizardActions.removeLocation} />
        <span className='chart-wizard__next' onClick={this.toggleStep('chart-type')}>Next</span>
      </div>
    )

    let chartTypeStep = (
      <div>
        <p className='chart-wizard__para'>What would the new chart look like?</p>
        <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
          onChange={ChartWizardActions.changeChart}/>
        <span className='chart-wizard__next' onClick={this.toggleStep('time-range')}>Next</span>
      </div>
    )

    let campaignListAsDate = _(this.state.data.campaignFilteredList).map(campaign => {
      return _.assign({}, campaign, {
        slug: moment(campaign.start_date).format('MMMM YYYY')
      })
    }).uniq(_.property('slug')).value()

    let timeRangeStep = (
      <div>
        <p className='chart-wizard__para'>Which time period would you like to display the data for?</p>
        <h4>Ending Time: </h4>
        <CampaignDropdownMenu
          text={this.state.data.campaign && moment(this.state.data.campaign.start_date).format('MMMM YYYY') || 'Select Ending Time'}
          campaigns={campaignListAsDate}
          sendValue={ChartWizardActions.addCampaign} />

        <RadioGroup name='time' title='Time Range'
          value={this.state.data.timeValue}
          values={this.state.data.timeRangeFilteredList} onChange={ChartWizardActions.changeTimeRadio} />
        <span className='chart-wizard__next' onClick={this.toggleStep('option')}>Next</span>
      </div>
    )

    let option = React.createElement(options[this.state.data.chartDef.type], {
      indicatorList: this.state.data.indicatorList,
      rawIndicators: this.state.data.rawIndicators,
      rawTags: this.state.data.rawTags,
      indicatorSelected: this.state.data.indicatorSelected,
      groupByValue: this.state.data.groupByValue,
      locationLevelValue: this.state.data.locationLevelValue,
      xFormatValue: this.state.data.xFormatValue,
      yFormatValue: this.state.data.yFormatValue,
      palette: this.state.data.chartDef.palette
    })

    let optionStep = (
      <div>
        {option}
        <span className='chart-wizard__next' onClick={this.toggleStep('preview')}>Next</span>
      </div>
    )

    let previewStep = (
      <div>
        <label>Title</label>
        <TitleInput initialText={this.state.data.chartDef.title} save={ChartWizardActions.editTitle}/>
        <span className='chart-wizard__save' onClick={this.saveChart}>
          {this.props.chartDef ? 'Update Chart' : 'Create Chart'}
        </span>
      </div>
    )

    let chart = (
      <Chart id='custom-chart' type={this.state.data.chartDef.type} data={this.state.data.chartData}
        options={this.state.data.chartOptions}/>
    )

    let countryName = this.state.data.countrySelected.map(country => country.name).join(', ')
    let locationName = this.state.data.location.map(location => location.name).join(', ')

    return (
      <div className='chart-wizard'>
        <ChartWizardStepList onToggle={this.toggleStep} active={this.state.refer}>
          <ChartWizardStep
            title={`1. Select Country${countryName.length > 0 ? ' - ' + countryName : ''}`}
            refer='country'>
            {countryStep}
          </ChartWizardStep>
          <ChartWizardStep
            title={`2. Select First Indicator${this.state.data.indicatorSelected[0] ? ' - ' + this.state.data.indicatorSelected[0].name : ''}`}
            refer='first-indicator'>
            {firstIndicatorStep}
          </ChartWizardStep>
          <ChartWizardStep title={`3. Select Location${locationName.length > 0 ? ' - ' + locationName : ''}`}
            refer='location'>
            {locationStep}
          </ChartWizardStep>
          <ChartWizardStep title='4. Select Chart Type' refer='chart-type'>
            {chartTypeStep}
          </ChartWizardStep>
          <ChartWizardStep
            title={`5. Select Time Range${this.state.data.campaign ? ' - ' + moment(this.state.data.campaign.start_date).format('MMMM YYYY') : ''}`}
            refer='time-range'>
            {timeRangeStep}
          </ChartWizardStep>
          <ChartWizardStep title='6. Customise Options' refer='option'>
            {optionStep}
          </ChartWizardStep>
          <ChartWizardStep title='7. Preview' refer='preview'>
            {previewStep}
          </ChartWizardStep>
        </ChartWizardStepList>
        <PreviewScreen isLoading={this.state.data.isLoading}>
          {this.state.data.canDisplayChart
            ? chart
            : (<div className='empty'>No Data</div>)
          }
        </PreviewScreen>
        <span className='chart-wizard__cancel' onClick={this.props.cancel}>Cancel</span>
      </div>
    )
  }
})

export default ChartWizard
