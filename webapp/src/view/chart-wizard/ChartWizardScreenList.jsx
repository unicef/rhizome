import React from 'react'

let ChartWizardScreenList = React.createClass({
  propTypes: {
    active: React.PropTypes.string,
  },

  render() {
    let children = this.props.children.map((item, idx) => {
      return React.addons.cloneWithProps(item, {
        active: this.props.active,
        key: idx
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
