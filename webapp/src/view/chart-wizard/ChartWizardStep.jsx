import React from 'react'

let ChartWizardStep = React.createClass({
  propTypes: {
    title: React.PropTypes.string,
    // onToggle: React.PropTypes.func,
    // active: React.PropTypes.string,
    // refer: React.PropTypes.string,
    children: React.PropTypes.element
  },

  getInitialState: function getInitialState () {
    return {
      isActive: false
    }
  },

  render () {
    let isActive = this.state.isActive
    return (
      <li className={'chart-wizard__step ' + (isActive ? 'active' : '')}>
        <h2 onClick={this.toggleStep}>
          {this.props.title}
          <i className={'fa ' + (isActive ? 'fa-minus' : 'fa-plus')}></i>
        </h2>
        <div className='chart-wizard__expandable'>
          {this.props.children}
        </div>
      </li>
    )
  },
  toggleStep () {
    var newActiveState = !(this.state.isActive)
    this.setState({isActive: newActiveState})
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return nextState.isActive !== this.state.isActive
  }
})

export default ChartWizardStep
