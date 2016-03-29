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

  _updateText: function () {
    let xAxisLabel = this.refs.xAxisLabel.getDOMNode().value
    let yAxisLabel = this.refs.yAxisLabel.getDOMNode().value
    this.props.onChange(xAxisLabel, yAxisLabel)
  },

  render: function () {
    return (
      <div>
        <label htmlFor='data-explorer-y-axis-label'> X Axis Label
          <input type='text' defaultValue={this.props.xLabel} onBlur={this._updateText} ref='xAxisLabel' id='data-explorer-y-axis-label' />
        </label>
        <label htmlFor='data-explorer-x-axis-label'> Y Axis Label
          <input type='text' defaultValue={this.props.yLabel} onBlur={this._updateText} ref='yAxisLabel' id='data-explorer-x-axis-label' />
        </label>
      </div>
    )
  }
})
