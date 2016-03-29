import React from 'react'
import _ from 'lodash'
import RadioGroup from 'components/molecules/RadioGroup.jsx'

let ScatterAxisChooser = React.createClass({
  propTypes: {
    xFormatValue: React.PropTypes.number,
    yFormatValue: React.PropTypes.number,
    formatValues: React.PropTypes.array,
    onXFormatChange: React.PropTypes.func,
    onYFormatChange: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      xFormatValue: 0,
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
          prefix='x-'
          value={this.props.xFormatValue}
          values={this.props.formatValues} onChange={this.props.onXFormatChange}/>
        <RadioGroup name='yFormat' title='Y Format: '
          prefix='y-'
          value={this.props.yFormatValue}
          values={this.props.formatValues} onChange={this.props.onYFormatChange}/>
      </div>
    )
  }
})

export default ScatterAxisChooser
