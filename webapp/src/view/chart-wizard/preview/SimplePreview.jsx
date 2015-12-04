import React from 'react'
import _ from 'lodash'

import TitleInput from 'component/TitleInput.jsx'
import PalettePicker from './PalettePicker.jsx'

export default class SimplePreview extends React.Component {
  constructor (props) {
    super(props)
  }

  static propTypes = {
    chartTitle: React.PropTypes.string,
    onEditTitle: React.PropTypes.func,
    palette: React.PropTypes.string,
    onChangePalette: React.PropTypes.func
  }

  static defaultProps = {
    chartTitle: null,
    onEditTitle: _.noop,
    palette: null,
    onChangePalette: _.noop
  }

  render () {
    return (
      <div>
        <label>Title</label>
        <TitleInput initialText={this.props.chartTitle} save={this.props.onEditTitle}/>
        <PalettePicker value={this.props.palette} onChange={this.props.onChangePalette}/>
      </div>
    )
  }
}

