import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'

let ScatterAxisChooser = React.createClass({

  propTypes: {
    indicatorArray: React.PropTypes.array,
    xValue: React.PropTypes.number,
    yValue: React.PropTypes.number,
    formatValues: React.PropTypes.array,
    onXFormatChange: React.PropTypes.func,
    onYFormatChange: React.PropTypes.func,
    onXAxisChange: React.PropTypes.func,
    onYAxisChange: React.PropTypes.func
  },

  getDefaultProps: function () {
    return {
      indicatorArray: [],
      xValue: 0,
      yValue: 0,
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

  componentDidMount() {
  },

  render() {
    let axisOptions = _(this.props.indicatorArray).map(function (indicator, index) {
      return <option key={indicator.id} value={index}>{indicator.name}</option>
    }).value();

    let chooseAxis = (<div>
      <div>
        <label>X Format</label>
        <RadioGroup name="xFormat" horizontal={true} value={this.props.xValue}
                    values={this.props.formatValues} onChange={this.props.onXFormatChange}/>
      </div>
      <div>
        <label>Y Format</label>
        <RadioGroup name="yFormat" horizontal={true} value={this.props.yValue}
                    values={this.props.formatValues} onChange={this.props.onYFormatChange}/>
      </div>
      <div>
        <label>X Axis</label>
        <select onChange={this._updateXAxis}>{axisOptions}</select></div>
      <div>
        <label>Y Axis</label>
        <select onChange={this._updateYAxis}>{axisOptions}</select></div>
    </div>)

    return chooseAxis
  }
})

export default ScatterAxisChooser