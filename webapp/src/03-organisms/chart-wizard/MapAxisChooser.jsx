import React from 'react'
import _ from 'lodash'
import RadioGroup from '02-molecules/RadioGroup.jsx'

let MapAxisChooser = React.createClass({
  propTypes: {
    colorFormatValue: React.PropTypes.number,
    onColorFormatChange: React.PropTypes.func,
    formatValues: React.PropTypes.array
  },

  getDefaultProps: function () {
    return {
      colorFormatValue: 0,
      onColorFormatChange: _.noop,
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
      </div>
    )
  }
})

export default MapAxisChooser
