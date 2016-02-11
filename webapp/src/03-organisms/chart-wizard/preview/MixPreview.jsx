import React from 'react'
import _ from 'lodash'

import TitleInput from '02-molecules/TitleInput.jsx'
import PalettePicker from './PalettePicker.jsx'
import XYAxisLabelSetter from './XYAxisLabelSetter.jsx'

export default class MixPreview extends React.Component {
  constructor (props) {
    super(props)
  }

  static propTypes = {
    chartTitle: React.PropTypes.string,
    onEditTitle: React.PropTypes.func,
    palette: React.PropTypes.string,
    onChangePalette: React.PropTypes.func,
    xLabel: React.PropTypes.string,
    yLabel: React.PropTypes.string,
    onSetXYAxisLabel: React.PropTypes.func
  }

  static defaultProps = {
    chartTitle: null,
    onEditTitle: _.noop,
    palette: null,
    onChangePalette: _.noop,
    xLabel: null,
    yLabel: null,
    onSetXYAxisLabel: _.noop
  }

  render () {
    return (
      <div>
        <label>Title</label>
        <TitleInput initialText={this.props.chartTitle} save={this.props.onEditTitle}/>
        <PalettePicker value={this.props.palette} onChange={this.props.onChangePalette}/>
        <XYAxisLabelSetter xLabel={this.props.xLabel} yLabel={this.props.yLabel} onChange={this.props.onSetXYAxisLabel} />
      </div>
    )
  }
}
