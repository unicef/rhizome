import React from 'react'

let ChartWizardStepList = React.createClass({
  render() {
    let children = this.props.children.map(item => {
      return React.addons.cloneWithProps(item, {
        onToggle: this.props.onToggle,
        active: this.props.active
      })
    })

    return (
      <ul className='chart-wizard__step-list'>
        {children}
      </ul>
    )
  }
})

export default ChartWizardStepList
