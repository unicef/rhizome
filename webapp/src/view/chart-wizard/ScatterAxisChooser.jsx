import React from 'react'
import _ from 'lodash'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'

let ScatterAxisChooser = React.createClass({
  propTypes: {
    indicatorArray: React.PropTypes.array,
    xAxisValue: React.PropTypes.number,
    xFormatValue: React.PropTypes.number,
    yAxisValue: React.PropTypes.number,
    yFormatValue: React.PropTypes.number,
    formatValues: React.PropTypes.array,
    onXFormatChange: React.PropTypes.func,
    onYFormatChange: React.PropTypes.func,
    onXAxisChange: React.PropTypes.func,
    onYAxisChange: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      indicatorArray: [],
      xAxisValue: 0,
      xFormatValue: 0,
      yAxisValue: 0,
      yFormatValue: 0,
      formatValues: [],
      onXFormatChange: _.noop,
      onYFormatChange: _.noop
    }
  },

  render () {
    return (
      <div>
        <RadioGroup name='xFormat' title='X Format: '
          value={this.props.xFormatValue}
          values={this.props.formatValues} onChange={this.props.onXFormatChange}/>
        <RadioGroup name='yFormat' title='Y Format: '
          value={this.props.yFormatValue}
          values={this.props.formatValues} onChange={this.props.onYFormatChange}/>
      </div>
    )
  }
})

export default ScatterAxisChooser
