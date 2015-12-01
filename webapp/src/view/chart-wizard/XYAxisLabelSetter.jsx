import React from 'react'
import _ from 'lodash'

export default React.createClass({
  propTypes: {
    xLabel: React.PropTypes.string,
    yLabel: React.PropTypes.string,
    onChange: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      xLabel: null,
      yLabel: null,
      onChange: _.noop
    }
  },

  getInitialState: function () {
    return {
      xLabel: null,
      yLabel: null
    }
  },

  componentWillReceiveProps: function (nextProps) {
    this.setState({xLabel: nextProps.xLabel, yLabel: nextProps.yLabel})
  },

  _updateText: function (e) {
    this.setState({xLabel: e.currentTarget.value})
    this.props.onChange(e.currentTarget.value)
  },
  render: function () {
    return (
      <div>
        <input type='text' value={this.state.xLabel} onChange={this._updateText}/>
        <input type='text' value={this.state.yLabel} onChange={this._updateText}/>
      </div>
    )
  }
})
