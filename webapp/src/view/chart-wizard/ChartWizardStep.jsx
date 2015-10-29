import React from 'react'

let ChartWizardStep = React.createClass({
  propTypes: {
    title: React.PropTypes.string,
    onToggle: React.PropTypes.func,
    active: React.PropTypes.string,
    refer: React.PropTypes.string
  },

  getInitialState() {
    return {
      title: this.props.title
    }
  },

  activeStep() {
    this.props.onToggle(this.props.refer)
  },

  render() {
    let isActive = this.props.active == this.props.refer ? 'active' : ''
    return (
      <li className={'chart-wizard__step ' + isActive}>
        <h2 onClick={this.activeStep}>{this.state.title}</h2>
        <div className='chart-wizard__expandable'>
          {this.props.children}
        </div>
      </li>
    )
  }
})

export default ChartWizardStep
