import React from 'react'

let ChartWizardStep = React.createClass({
  propTypes: {
    title: React.PropTypes.string,
    onToggle: React.PropTypes.func,
    active: React.PropTypes.string,
    refer: React.PropTypes.string
  },

  activeStep() {
    this.props.onToggle(this.props.refer)
  },

  render() {
    let isActive = this.props.active == this.props.refer ? 'active' : ''
    return (
      <li className={'chart-wizard__step ' + isActive}>
        <h2 onClick={this.activeStep}>{this.props.title}</h2>
        <div className='chart-wizard__expandable'>
          {this.props.children}
        </div>
      </li>
    )
  }
})

ab=addDeclaredGlobals;21223;[3;32]

export default ChartWizardStep
