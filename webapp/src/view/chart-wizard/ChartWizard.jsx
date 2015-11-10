import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'

import ChartWizardStep from './ChartWizardStep.jsx'
import ChartWizardStepList from './ChartWizardStepList.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import MenuItem from 'component/MenuItem.jsx'
import DropdownMenu from 'component/DropdownMenu.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import CampaignDropdownMenu from 'component/CampaignDropdownMenu.jsx'
import List from 'component/list/List.jsx'
import TitleInput from 'component/TitleInput.jsx'
import Chart from 'component/Chart.jsx'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'
import ChartSelect from '../chart-builder/ChartSelect.jsx'
import ScatterAxisChooser from './ScatterAxisChooser.jsx'

import ChartWizardActions from 'actions/ChartWizardActions'
import ChartWizardStore from 'stores/ChartWizardStore'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'

const defaultChartDef = {
  title: '',
  type: 'LineChart',
  indicators: [],
  groupBy: 'indicator',
  timeRange: null,
  x: 0,
  xFormat: ',.0f',
  y: 0,
  yFormat: ',.0f'
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

function findChartType (type) {
  return builderDefinitions.charts[_.findIndex(builderDefinitions.charts, {name: type})] || {}
}

let ChartWizard = React.createClass({
  mixins: [Reflux.connect(ChartWizardStore, 'data')],

  propTypes: {
    save: React.PropTypes.func,
    cancel: React.PropTypes.func
  },

  getInitialState () {
    return {
      refer: 'location'
    }
  },

  componentDidMount () {
    this.chartDef = this.props.chartDef || defaultChartDef
    ChartWizardActions.initialize(this.chartDef)
  },

  saveChart () {
    ChartWizardActions.saveChart(this.props.save)
  },

  toggleStep (refer) {
    this.setState({
      refer: refer
    })
  },

  setLocationSearch (pattern) {
    this.setState({
      locationSearch: pattern
    })
  },

  render () {
    let locations = MenuItem.fromArray(filterMenu(this.state.data.locationList, this.state.locationSearch), ChartWizardActions.addLocation)

    let locationStep = (
      <div>
        <p className='chart-wizard__para'>Which country's data will the new chart visualise?</p>
        <DropdownMenu
          icon='fa-globe'
          text={this.state.data.location && this.state.data.location.name || 'Select Location'}
          searchable={true}
          onSearch={this.setLocationSearch}>
          {locations}
        </DropdownMenu>
        <span className='chart-wizard__next' onClick={this.toggleStep.bind(null, 'indicator')}>Next</span>
      </div>
    )

    let indicatorStep = (
      <div>
        <p className='chart-wizard__para'>Which indicators will be included in the new chart?</p>
        <IndicatorDropdownMenu
          text='Add Indicators'
          icon='fa-plus'
          indicators={this.state.data.indicatorList}
          sendValue={ChartWizardActions.addIndicator}>
        </IndicatorDropdownMenu>
        <List items={this.state.data.indicatorSelected} removeItem={ChartWizardActions.removeIndicator}/>
        <span className='chart-wizard__next' onClick={this.toggleStep.bind(null, 'chart-type')}>Next</span>
      </div>
    )

    let chartTypeStep = (
      <div>
        <p className='chart-wizard__para'>What would the new chart look like?</p>
        <ChartSelect charts={this.state.data.chartTypeFilteredList} value={this.state.data.chartDef.type}
          onChange={ChartWizardActions.changeChart}/>
        <span className='chart-wizard__next' onClick={this.toggleStep.bind(null, 'time-range')}>Next</span>
      </div>
    )

    let campaignListAsDate = this.state.data.campaignFilteredList.map(campaign => {
      return _.assign({}, campaign, {
        slug: moment(campaign.start_date).format('MMMM YYYY')
      })
    })

    let timeRangeStep = (
      <div>
        <p className='chart-wizard__para'>Which time period would you like to display the data for?</p>
        <h4>Ending Time: </h4>
        <CampaignDropdownMenu
          text={this.state.data.campaign && moment(this.state.data.campaign.start_date).format('MMMM YYYY') || 'Select Campaign'}
          campaigns={campaignListAsDate}
          sendValue={ChartWizardActions.addCampaign}>
        </CampaignDropdownMenu>

        <RadioGroup name='time' title='Time Range'
          value={this.state.data.timeValue}
          values={this.state.data.timeRangeFilteredList} onChange={ChartWizardActions.changeTimeRadio} />
        <span className='chart-wizard__next' onClick={this.toggleStep.bind(null, 'option')}>Next</span>
      </div>
    )

    let groupBy = (
      <RadioGroup name='groupby' title='Group By: '
        value={this.state.data.groupByValue}
        values={builderDefinitions.groups} onChange={ChartWizardActions.changeGroupRadio} />
    )
    let locationLevel = (
      <RadioGroup name='location-level' title='Location Level: '
        value={this.state.data.locationLevelValue}
        values={builderDefinitions.locationLevels}
        onChange={ChartWizardActions.changeLocationLevelRadio}/>
    )

    let optionStep = (
      <div>
        <p className='chart-wizard__para'>You may also change additional chart settings.</p>
        {findChartType(this.state.data.chartDef.type).groupBy ? groupBy : null}
        {findChartType(this.state.data.chartDef.type).locationLevel ? locationLevel : null}
        {findChartType(this.state.data.chartDef.type).chooseAxis
          ? (
            <ScatterAxisChooser xAxisValue = {this.state.data.chartDef.x}
              xFormatValue={this.state.data.xFormatValue}
              onXFormatChange={ChartWizardActions.changeXFormatRadio}
              yAxisValue={this.state.data.chartDef.y}
              yFormatValue={this.state.data.yFormatValue}
              onYFormatChange={ChartWizardActions.changeYFormatRadio}
              formatValues={builderDefinitions.formats}
              indicatorArray={this.state.data.indicatorSelected}
              onXAxisChange={ChartWizardActions.changeXAxis}
              onYAxisChange={ChartWizardActions.changeYAxis}
            />
          )
          : (
            <RadioGroup name='format' title='Format: '
              value={this.state.data.yFormatValue}
              values={builderDefinitions.formats} onChange={ChartWizardActions.changeYFormatRadio} />
          )
        }
        <span className='chart-wizard__next' onClick={this.toggleStep.bind(null, 'preview')}>Next</span>
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

    return (
      <div className='chart-wizard'>
        <ChartWizardStepList onToggle={this.toggleStep} active={this.state.refer}>
          <ChartWizardStep title={`1. Select Location - ${this.state.data.location && this.state.data.location.name}`}
            refer='location'>
            {locationStep}
          </ChartWizardStep>
          <ChartWizardStep title='2. Select Indicator' refer='indicator'>
            {indicatorStep}
          </ChartWizardStep>
          <ChartWizardStep title='3. Select Chart Type' refer='chart-type'>
            {chartTypeStep}
          </ChartWizardStep>
          <ChartWizardStep title='4. Select Time Range' refer='time-range'>
            {timeRangeStep}
          </ChartWizardStep>
          <ChartWizardStep title='5. Customise Options' refer='option'>
            {optionStep}
          </ChartWizardStep>
          <ChartWizardStep title='6. Preview' refer='preview'>
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
