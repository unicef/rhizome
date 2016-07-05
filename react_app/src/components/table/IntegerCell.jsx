import _ from 'lodash'
import React, {Component} from 'react'
import DropdownButton from 'components/button/DropdownButton'

class IntegerCell extends Component {
  constructor (props) {
    super(props)
    this.state = {
    	editMode: false,
      display_value: props.cellParams.datapoint.display_value
    }
  }

	componentDidUpdate = () => {
		if (this.state.editMode) {
			this.refs.cell_input.focus()
		}
	}

  _handleInput = e => {
  	const value = e.target.value
  	const valueChanged = parseInt(this.state.display_value) !== parseInt(value)
  	if (e.keyCode && e.keyCode === 27) {
  		return this._toggleEditMode()
  	}
  	if ((e.keyCode && e.keyCode === 13) || !e.keyCode) {
	  	return valueChanged ? this._updateCell(value) : this._toggleEditMode()
  	}
  }

  _updateCell = value => {
  	const new_datapoint = Object.assign({}, this.props.cellParams.datapoint, {value})
    if (new_datapoint.id && _.isEmpty(value)) {
      this.props.cellParams.removeDatapoint(new_datapoint)
    } else if (new_datapoint.id && value) {
      this.props.cellParams.updateDatapoint(new_datapoint)
    } else if (!(new_datapoint.id && value)) {
      return this._toggleEditMode()
    }
    this.setState({ editMode: false, display_value: value })
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
    			defaultValue={this.state.display_value}
    			onBlur={this._handleInput}
    			onKeyUp={this._handleInput}
    		/>
    	)
    }
    return (
    	<div style={{width: '100%', height: '1.5rem'}} onClick={this._toggleEditMode}>
    		{this.state.display_value}
    	</div>
    )
  }
}


export default IntegerCell