import React from 'react'
import _ from 'lodash'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'

let MapAxisChooser = React.createClass({
  propTypes: {
    bubbleFormatValue: React.PropTypes.number,
    formatValues: React.PropTypes.array,
    onBubbleFormatChange: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      bubbleFormatValue: 0,
      formatValues: [],
      onBubbleFormatChange: _.noop
    }
  },

  render () {
    return (
      <div>
        <RadioGroup name='bubbleFormat' title='Bubble Format: '
          prefix='bubble-'
          value={this.props.bubbleFormatValue}
          values={this.props.formatValues} onChange={this.props.onBubbleFormatChange}/>
      </div>
    )
  }
})

export default MapAxisChooser
