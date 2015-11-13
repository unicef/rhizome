'use strict'

import React from 'react'

import dom from 'util/dom'

var Search = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func.isRequired,

    autoFocus: React.PropTypes.bool,
    onBlur: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      autoFocus: false,
      onBlur: function () {} // noop
    }
  },

  getInitialState: function () {
    return {
      pattern: ''
    }
  },

  render: function () {
    var clear = this.state.pattern.length > 0
      ? (
        <a className='clear-btn' tabIndex='-1' onClick={this._clear}>
          <i className='fa fa-times-circle'></i>
        </a>
      )
      : null

    return (
      <div style={{ position: 'relative' }} role='search'>
        <input ref='input' type='text' tabIndex='1'
          onChange={this._setPattern}
          onBlur={this._onBlur}
          value={this.state.pattern} />
        {clear}
      </div>
    )
  },

  componentDidMount: function () {
    if (this.props.autoFocus) {
      this._focus()
    }
  },

  _setPattern: function (e) {
    this.props.onChange(e.target.value)
    this.setState({ pattern: e.target.value })
  },

  _clear: function () {
    this.props.onChange('')
    this.setState({ pattern: '' })
    this._focus()
  },

  _focus: function () {
    React.findDOMNode(this.refs.input).focus()
  },

  _onBlur: function () {
    var self = this

    window.setTimeout(function () {
      if (dom.parentOf(React.findDOMNode(self), document.activeElement)) {
        self._focus()
      } else {
        self.props.onBlur()
      }
    }, 150)
  }
})

export default Search
