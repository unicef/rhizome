import React from 'react'
import _ from 'lodash'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'

let MapAxisChooser = React.createClass({
  propTypes: {
    colorFormatValue: React.PropTypes.number,
    onColorFormatChange: React.PropTypes.func,
    bubbleFormatValue: React.PropTypes.number,
    onBubbleFormatChange: React.PropTypes.func,
    formatValues: React.PropTypes.array
  },

  getDefaultProps: function () {
    return {
      colorFormatValue: 0,
      onColorFormatChange: _.noop,
      bubbleFormatValue: 0,
      onBubbleFormatChange: _.noop,
      formatValues: []
    }
  },

  render () {
    return (
      <div>
        <RadioGroup name='colorFormat' title='Color Format: '
          prefix='color-'
          value={this.props.colorFormatValue}
          values={this.props.formatValues} onChange={this.props.onColorFormatChange}/>
        <RadioGroup name='bubbleFormat' title='Bubble Format: '
          prefix='bubble-'
          value={this.props.bubbleFormatValue}
          values={this.props.formatValues} onChange={this.props.onBubbleFormatChange}/>
      </div>
    )
  }
})

export default MapAxisChooser
