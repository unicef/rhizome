import React from 'react'

let ChartWizardStep = React.createClass({
  propTypes: {
    title: React.PropTypes.string,
    onToggle: React.PropTypes.func,
    active: React.PropTypes.string,
    refer: React.PropTypes.string,
    children: React.PropTypes.element
  },

  activeStep () {
    this.props.onToggle(this.props.refer)
  },

  render () {
    let isActive = this.props.active === this.props.refer
    return (
      <li className={'chart-wizard__step ' + (isActive ? 'active' : '')}>
        <h2 onClick={this.activeStep}>
          {this.props.title}
          <i className={'fa ' + (isActive ? 'fa-minus' : 'fa-plus')}></i>
        </h2>
        <div className='chart-wizard__expandable'>
          {this.props.children}
        </div>
      </li>
    )
  }
})

export default ChartWizardStep
