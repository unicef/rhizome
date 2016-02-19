import React from 'react'
import _ from 'lodash'

var CSVMenuItem = React.createClass({
  propTypes: {
    sendValue: React.PropTypes.func.isRequired,
    title: React.PropTypes.string.isRequired,
    value: React.PropTypes.string.isRequired,
    depth: React.PropTypes.number,
    filtered: React.PropTypes.bool,
    noValue: React.PropTypes.bool
  },

  statics: {
    fromArray: function (arr, sendValue, depth) {
      if (!_.isFinite(depth)) {
        depth = 0
      }

      return arr.map(item => {
        return (
          <CSVMenuItem
            key={item.value}
            depth={depth}
            sendValue={sendValue}
            {...item} />
        )
      })
    }
  },

  _toggleChildren: function (e) {
    e.stopPropagation()
    this.setState({open: !this.state.open})
  },

  _handleClick: function (e) {
    if (!this.props.noValue) {
      this.props.sendValue(this.props.value)
    } else {
      this._toggleChildren(e)
    }
  },

  render: function () {
    return (
      <div onClick={this._handleClick} className='button csv-upload__button'>
        {this.props.title}
      </div>
    )
  }
})

export default CSVMenuItem
