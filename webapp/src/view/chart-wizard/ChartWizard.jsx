import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'

import ChartWizardStep from './ChartWizardStep.jsx'
import ChartWizardStepList from './ChartWizardStepList.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import List from 'component/list/List.jsx'
import Chart from 'component/Chart.jsx'
import ChartSelect from '../chart-builder/ChartSelect.jsx'

import ChartWizardActions from 'actions/ChartWizardActions'
import ChartWizardStore from 'stores/ChartWizardStore'
import chartDefinitions from 'stores/chartBuilder/chartDefinitions'

const defaultChartDef = {
  type: 'LineChart',
  indicators: [],
  groupBy: 'indicator',
  timeRange: null,
  x: 0,
  xFormat: ',.0f',
  y: 0,
  yFormat: ',.0f'
}

let ChartWizard = React.createClass({
  mixins: [Reflux.connect(ChartWizardStore, 'data')],

  propTypes: {
    save: React.PropTypes.func,
    cancel: React.PropTypes.func
  },

  getInitialState() {
    return {
      refer: 'country',
      title: this.props.chartDef ? this.props.chartDef.title : ''
    }
  },

  componentDidMount() {
    this.chartDef = this.props.chartDef || defaultChartDef
    ChartWizardActions.initialize(this.chartDef, this.props.location, this.props.campaign)
  },

  createChart() {
    let chart = _.merge(this.chartDef, {
      title: this.state.title,
      type: this.state.data.chartType,
      indicators: this.state.data.indicatorSelected.map(item => {
        return item.id
      })
    }, (a, b) => {
      return b
    })

    this.props.save(chart)
  },

  editTitle(e) {
    let title = e.target.value
    this.setState({
      title: title
    })
  },

  toggleStep(refer) {
    this.setState({
      refer: refer
    })
  },

  render() {
    let previewStep = (
      <div>
        <label>Title</label>
        <input type='text' value={this.state.title} onChange={this.editTitle} />
        <a href="#" className="button success" onClick={this.createChart}>
          {this.props.chartDef ? "Update Chart" : "Create Chart"}
        </a>
      </div>
    )

    let indicatorStep = (
      <div>
        <IndicatorDropdownMenu
          text='Add Indicators'
          icon='fa-plus'
          indicators={this.state.data.indicatorList}
          sendValue={ChartWizardActions.addIndicator}>
        </IndicatorDropdownMenu>
        <List items={this.state.data.indicatorSelected} removeItem={ChartWizardActions.removeIndicator} />
      </div>
    )

    let chartTypeStep = (
      <div>
        <ChartSelect charts={chartDefinitions} value={this.state.data.chartType}
          onChange={ChartWizardActions.changeChart}/>
      </div>
    )

    let chart = (
      <Chart id="custom-chart" type={this.state.data.chartType} data={this.state.data.chartData} options={this.state.data.chartOptions}/>
    )

    return (
      <div className='chart-wizard'>
        <ChartWizardStepList onToggle={this.toggleStep} active={this.state.refer}>
          <ChartWizardStep title='Select Country' refer='country'>
            <p>select country here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Indicator' refer='indicator'>
            {indicatorStep}
          </ChartWizardStep>
          <ChartWizardStep title='Select Location' refer='location'>
            <p>select location here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Campaign' refer='campaign'>
            <p>select campaign here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Chart Type' refer='chart-type'>
            {chartTypeStep}
          </ChartWizardStep>
          <ChartWizardStep title='Customise Styles' refer='style'>
            <p>Customise styles here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Preview' refer='preview'>
            {previewStep}
          </ChartWizardStep>
        </ChartWizardStepList>
        <PreviewScreen>
          {this.state.data.canDisplayChart ? chart : null}
        </PreviewScreen>
        <a className='chart-wizard__cancel' href="#" onClick={this.props.cancel}>Cancel without saving chart</a>
      </div>
    )
  }
})

export default ChartWizard
