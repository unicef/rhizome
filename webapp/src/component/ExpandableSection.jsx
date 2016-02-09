import React from 'react'

let ExpandableSection = React.createClass({
  propTypes: {
    title: React.PropTypes.string,
    children: React.PropTypes.element
  },

  getInitialState: function () {
    return { isActive: false }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return nextState.isActive !== this.state.isActive || this.props.children !== nextProps.children
  },

  toggleStep: function () {
    var newActiveState = !(this.state.isActive)
    this.setState({isActive: newActiveState})
  },

  render: function () {
    let isActive = this.state.isActive
    return (
      <li className={'expandable-section ' + (isActive ? 'active' : '')}>
        <h2 onClick={this.toggleStep}>
          {this.props.title}
          <i className={'fa ' + (isActive ? 'fa-minus' : 'fa-plus')}></i>
        </h2>
        <div className='expandable-section__body'>
          {this.props.children}
        </div>
      </li>
    )
  }
})

export default ExpandableSection
