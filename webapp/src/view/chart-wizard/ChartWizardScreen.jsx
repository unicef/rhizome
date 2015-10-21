import React from 'react'

let ChartWizardScreen = React.createClass({
  propTypes: {
    active: React.PropTypes.string,
    referTo: React.PropTypes.string
  },

  render() {
    let isActive = this.props.active == this.props.referTo ? 'active' : ''
    return (
      <div className={'chart-wizard__screen ' + isActive}>
        {this.props.children}
      </div>
    )
  }
})

export default ChartWizardScreen
