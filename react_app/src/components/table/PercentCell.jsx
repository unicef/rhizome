import React, {Component} from 'react'

class PercentCell extends Component {
	constructor (props) {
		super(props)
		this.state = {
			editMode: false
		}
	}

	toggleEditMode = () => {
		this.setState({editMode: !this.state.editMode})
	}

	componentDidUpdate(prevProps, prevState) {
		const datapoint = this.props.cellParams.datapoint
		if (this.state.editMode) {
			this.refs.da_input.focus()
		}
	}

	render = () => {
		const params = this.props.cellParams.params
		const datapoint = this.props.cellParams.datapoint
		if (this.state.editMode) {
			return <input onBlur={this.toggleEditMode} ref='da_input' type='text' value={datapoint.value}></input>
		}
	  return <span onClick={this.toggleEditMode}>{datapoint.display_value}</span>
	}
}

export default PercentCell