import _ from 'lodash'
import React, {Component} from 'react'
import DropdownButton from 'components/button/DropdownButton'
import format from 'utilities/format'

class PercentCell extends Component {
  constructor (props) {
    super(props)
    this.data_format = this.props.cellParams.datapoint.indicator.data_format
    this.state = {
    	editMode: false,
      datapoint: Object.assign({}, props.cellParams.datapoint)
    }
  }

	componentDidUpdate = () => {
		if (this.state.editMode) {
			this.refs.cell_input.focus()
		}
	}

  _handleInput = e => {
    const old_value = this.data_format === 'pct' ? this.state.datapoint.value : parseInt(this.state.datapoint.value)
    const new_value = this._parseNewValue(e.target.value)
  	if (e.keyCode && e.keyCode === 27) {
  		return this._toggleEditMode()
  	}
  	if ((e.keyCode && e.keyCode === 13) || !e.keyCode) {
	  	old_value !== new_value ? this._updateCell(new_value) : this._toggleEditMode()
  	}
  }

  _updateCell = value => {
    const display_value = format.autoFormat(value, this.data_format)
  	const new_datapoint = Object.assign({}, this.state.datapoint, {value, display_value})
    if (new_datapoint.id && value === null) {
      this.props.cellParams.removeDatapoint(new_datapoint)
    } else {
      this.props.cellParams.updateDatapoint(new_datapoint)
    }
    this.setState({ editMode: false, datapoint: new_datapoint})
  }

  _parseNewValue = value => {
    if (this.data_format === 'pct') {
      return value ? value / 100 : null
    } else {
      return value ? parseInt(value) : null
    }
  }

  _getInitialInputValue = () => {
    if (this.data_format === 'pct') {
      return this.state.datapoint.value ? (this.state.datapoint.value * 100).toFixed(0) : null
    } else {
      return this.state.datapoint.display_value
    }
  }

  _toggleEditMode = () => {
  	this.setState({editMode: !this.state.editMode})
  }

  render = () => {
    if (this.state.editMode) {
    	return (
    		<input
    			type='text'
    			ref='cell_input'
    			defaultValue={this._getInitialInputValue()}
    			onBlur={this._handleInput}
    			onKeyUp={this._handleInput}
    		/>
    	)
    }
    return (
    	<div style={{width: '100%', height: '1.5rem'}} onClick={this._toggleEditMode}>
    		{this.state.datapoint.display_value}
    	</div>
    )
  }
}


export default PercentCell