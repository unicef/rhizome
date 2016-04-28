import React, {Component, PropTypes} from 'react'
import format from 'utilities/format'
import palettes from 'utilities/palettes'

class DatapointTableCell extends Component {

  propTypes = {
    datapoint: PropTypes.object,
    indicator: PropTypes.indicator,
    onSave: PropTypes.func,
  }

  constructor (props) {
    super(props)
    this.state = {
      editMode: false
    }
  }

  enterEditMode = function (event) {
    if (!this.props.onSave) { return }
    this.setState({ editMode: true })
  }

  determineCellColor = function () {
    const value = this.props.datapoint.value
    const good_bound = this.props.indicator.good_bound
    const bad_bound = this.props.indicator.bad_bound
    const palette = good_bound > bad_bound ? palettes['traffic_light'] : palettes['traffic_light'].reverse()
    if (value < bad_bound && value > good_bound ) {
      return palette[1] // yellow
    } else if (value <= bad_bound) {
      return palette[0] // red
    }
    return palette[2] // green
  }

  renderCellContent = function () {
    const data_format = this.props.indicator.data_format
    const value = this.props.datapoint.value
    const display_value = format.autoFormat(value, data_format)

    if (data_format === 'pct') {
      return (
        <div className='percent-bar'>
          <div style={{width: display_value, background: this.determineCellColor()}}>
            {display_value}
          </div>
        </div>
      )
    }
    return {display_value}
  }

  render = function () {
    const key = 'cell-' + this.props.datapoint.computed
    if (!this.state.editMode) {
      return (
        <td key={key} onClick={this.enterEditMode}>
          { this.renderCellContent() }
        </td>
      )
    } else {
      return (
        <td key={key}>
          <input type='text'/>
        </td>
      )
    }
  }
}

export default DatapointTableCell
