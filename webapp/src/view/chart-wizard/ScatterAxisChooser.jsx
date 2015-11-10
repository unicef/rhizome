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
      onYFormatChange: _.noop,
      onXAxisChange: _.noop,
      onYAxisChange: _.noop
    }
  },

  _updateXAxis (e) {
    this.props.onXAxisChange(parseInt(e.target.value, 10))
  },

  _updateYAxis (e) {
    this.props.onYAxisChange(parseInt(e.target.value, 10))
  },

  render () {
    let self = this
    let axisOptions = function (selectedValue, updateXAxis) {
      var hasSelected = false
      let result = self.props.indicatorArray.map(indicator => {
        let selected = selectedValue === indicator.id
        if (!hasSelected && selected) hasSelected = true
        return <option value={indicator.id} selected={selected}>{indicator.name}</option>
      })
      if (!hasSelected && self.props.indicatorArray.length > 0) updateXAxis(self.props.indicatorArray[0].id)
      return result
    }

    return (
      <div>
        <RadioGroup name='xFormat' title='X Format: '
          value={this.props.xFormatValue}
          values={this.props.formatValues} onChange={this.props.onXFormatChange}/>
        <RadioGroup name='yFormat' title='Y Format: '
          value={this.props.yFormatValue}
          values={this.props.formatValues} onChange={this.props.onYFormatChange}/>
        <div>
          <label>X Axis</label>
          <select onChange={this._updateXAxis}>{axisOptions(this.props.xAxisValue, this.props.onXAxisChange)}</select></div>
        <div>
          <label>Y Axis</label>
          <select onChange={this._updateYAxis}>{axisOptions(this.props.yAxisValue, this.props.onYAxisChange)}</select></div>
      </div>
    )
  }
})

export default ScatterAxisChooser
