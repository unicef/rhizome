import React from 'react'

let ChartWizardScreenList = React.createClass({
  render() {
    let children = this.props.children.map(item => {
      return React.addons.cloneWithProps(item, {
        active: this.props.active
      })
    })
    return (
      <div className='chart-wizard__screen-list'>
        {children}
      </div>
    )
  }
})

export default ChartWizardScreenList
