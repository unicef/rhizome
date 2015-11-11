'use strict'

var _ = require('lodash')
var React = require('react')

var dom = require('util/dom')

var Tooltip = React.createClass({
  propTypes: {
    top: React.PropTypes.number.isRequired,
    left: React.PropTypes.number.isRequired
    // children: React.PropTypes.array
  },

  getInitialState: function () {
    return {
      align: 'left',
      orient: 'top'
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return !(_.isEqual(this.props, nextProps) && _.isEqual(this.state, nextState))
  },

  render: function () {
    var position = {}

    if (this.state.align === 'left') {
      position.left = this.props.left
    } else {
      position.right = document.body.clientWidth - this.props.left
    }

    if (this.state.orient === 'top') {
      position.top = this.props.top
    } else {
      position.bottom = document.body.clientHeight - this.props.top
    }

    return (
      <div className='tooltip' style={position}>
        {this.props.children}
      </div>
    )
  },

  componentDidUpdate: function () {
    this._reposition()
  },

  componentDidMount: function () {
    window.requestAnimationFrame(this._reposition)
  },

  _reposition: function () {
    if (!this.isMounted()) {
      return
    }

    var el = dom.dimensions(React.findDOMNode(this))
    var state = { align: 'left', orient: 'top' }

    if (this.props.left - window.pageXOffset > window.innerWidth / 2) {
      // state.align = 'right' // fix the tooltip position incorrect issue.
    }

    //
    if (this.props.top - window.pageYOffset + el.height > window.innerHeight) {
      // state.orient = 'bottom' // fix the tooltip position incorrect issue.
    }

    this.setState(state)
  }
})

module.exports = Tooltip
