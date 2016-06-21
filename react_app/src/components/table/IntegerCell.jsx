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
  	this.props.cellParams.updateDatapoint(new_datapoint)
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
    	<span onClick={this._toggleEditMode}>
    		{this.state.display_value}
    	</span>
    )
  }
}


export default IntegerCell