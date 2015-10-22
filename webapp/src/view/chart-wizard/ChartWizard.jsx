import React from 'react'

import ChartWizardStep from './ChartWizardStep.jsx'
import ChartWizardStepList from './ChartWizardStepList.jsx'
import PreviewScreen from './PreviewScreen.jsx'

let ChartWizard = React.createClass({
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

  createChart() {
    this.props.chartDef.title = this.state.title
    this.props.save(this.props.chartDef)
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

    return (
      <div className='chart-wizard'>
        <ChartWizardStepList onToggle={this.toggleStep} active={this.state.refer}>
          <ChartWizardStep title='Select Country' refer='country'>
            <p>select country here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Indicator' refer='indicator'>
            <p>select indicators here</p>
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
