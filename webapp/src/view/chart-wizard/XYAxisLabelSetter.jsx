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

  _updateText: function () {
    let xAxisLabel = this.refs.xAxisLabel.getDOMNode().value
    let yAxisLabel = this.refs.yAxisLabel.getDOMNode().value
    this.setState({xLabel: xAxisLabel, yLabel: yAxisLabel})
    this.props.onChange(xAxisLabel, yAxisLabel)
  },
  render: function () {
    return (
      <div>
        <label htmlFor='chart-wizard-y-axis-label'> X Axis Label
          <input type='text' value={this.state.xLabel} onChange={this._updateText} ref='xAxisLabel' id='chart-wizard-y-axis-label' />
        </label>
        <label htmlFor='chart-wizard-x-axis-label'> Y Axis Label
          <input type='text' value={this.state.yLabel} onChange={this._updateText} ref='yAxisLabel' id='chart-wizard-x-axis-label' />
        </label>
      </div>
    )
  }
})
