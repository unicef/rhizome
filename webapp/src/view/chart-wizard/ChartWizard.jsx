import React from 'react'

import ChartWizardStep from './ChartWizardStep.jsx'

const chartDef = {"title":"Polio Case","type":"LineChart","indicators":[168],"locations":"selected","groupBy":"indicator","x":0,"y":0,"xFormat":",.0f","yFormat":",.0f","timeRange":null,"id":22}

let ChartWizard = React.createClass({
  getInitialState() {
    return {
      refer: null
    }
  },

  createChart() {
    this.props.save(chartDef)
  },

  activeStep(refer) {
    this.setState({
      refer: refer
    })
  },

  render() {
    let previewStep = (
      <div>
        <input type='text' value={chartDef.title} />
        <a href="#" className="button success" onClick={this.createChart}>
          {this.props.chartDef ? "Update Chart" : "Create Chart"}
        </a>
      </div>
    )

    return (
      <div className='chart-wizard'>
        <ul className='chart-wizard__step-list'>
          <ChartWizardStep title='Select Country' refer='country' onToggle={this.activeStep} active={this.state.refer}>
            <p>select country here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Indicator' refer='indicator' onToggle={this.activeStep} active={this.state.refer}>
            <p>select indicators here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Location' refer='location' onToggle={this.activeStep} active={this.state.refer}>
            <p>select location here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Campaign' refer='campaign' onToggle={this.activeStep} active={this.state.refer}>
            <p>select campaign here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Select Chart Type' refer='chart-type' onToggle={this.activeStep} active={this.state.refer}>
            <p>select chart type here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Customise Styles' refer='style' onToggle={this.activeStep} active={this.state.refer}>
            <p>Customise styles here</p>
          </ChartWizardStep>
          <ChartWizardStep title='Preview' refer='preview' onToggle={this.activeStep} active={this.state.refer}>
            {previewStep}
          </ChartWizardStep>
        </ul>
      </div>
    )
  }
})

export default ChartWizard
