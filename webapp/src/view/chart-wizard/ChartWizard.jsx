import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'

import ChartWizardStep from './ChartWizardStep.jsx'
import ChartWizardStepList from './ChartWizardStepList.jsx'
import PreviewScreen from './PreviewScreen.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import List from 'component/list/List.jsx'

import ChartWizardActions from 'actions/ChartWizardActions'
import ChartWizardStore from 'stores/ChartWizardStore'

let ChartWizard = React.createClass({
  mixins: [Reflux.connect(ChartWizardStore, 'data')],

  propTypes: {
    save: React.PropTypes.func,
    cancel: React.PropTypes.func
  },

  getInitialState() {
    return {
      refer: 'country',
      title: this.props.chartDef.title
    }
  },

  componentDidMount() {
    ChartWizardActions.initialize(this.props.chartDef)
  },

  createChart() {
    let chart = _.merge(this.props.chartDef, {
      title: this.state.title,
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
            <p>select chart type here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Customise Styles' refer='style'>
            <p>Customise styles here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Preview' refer='preview'>
            {previewStep}
          </ChartWizardStep>
        </ChartWizardStepList>
        <PreviewScreen />
        <a className='chart-wizard__cancel' href="#" onClick={this.props.cancel}>Cancel without saving chart</a>
      </div>
    )
  }
})

export default ChartWizard
