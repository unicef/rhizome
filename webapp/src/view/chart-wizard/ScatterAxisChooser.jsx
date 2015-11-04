import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'
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

  _updateXAxis(e){
    this.props.onXAxisChange(parseInt(e.target.value))
  },

  _updateYAxis(e){
    this.props.onYAxisChange(parseInt(e.target.value))
  },

  render() {
    let self = this
    let axisOptions = function (selectedValue, updateXAxis) {
      var selected = false
      let result = _(self.props.indicatorArray).map(function (indicator) {
        if (!selected) selected = selectedValue === indicator.id
        return <option value={indicator.id} selected={selectedValue === indicator.id}>{indicator.name}</option>
      }).value()
      if (!selected && self.props.indicatorArray.length > 0)
        updateXAxis(self.props.indicatorArray[0].id)
      return result
    }

    return (
      <div>
        <div>
          <label>X Format</label>
          <RadioGroup name="xFormat" horizontal={true} value={this.props.xFormatValue}
                      values={this.props.formatValues} onChange={this.props.onXFormatChange}/>
        </div>
        <div>
          <label>Y Format</label>
          <RadioGroup name="yFormat" horizontal={true} value={this.props.yFormatValue}
                      values={this.props.formatValues} onChange={this.props.onYFormatChange}/>
        </div>
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
