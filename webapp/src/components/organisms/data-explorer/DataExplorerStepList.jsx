import React from 'react'

let DataExplorerStepList = React.createClass({
  propTypes: {
    active: React.PropTypes.string,
    onToggle: React.PropTypes.func,
    children: React.PropTypes.arrayOf(React.PropTypes.element)
  },

  render () {
    let children = this.props.children.map((item, idx) => {
      return React.addons.cloneWithProps(item, {
        onToggle: this.props.onToggle,
        active: this.props.active,
        key: idx
      })
    })

    return (
      <ul className='data-explorer__step-list'>
        {children}
      </ul>
    )
  }
})

export default DataExplorerStepList
