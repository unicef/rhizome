import React, {Component} from 'react'
import DropdownButton from 'components/button/DropdownButton'

class BoolCell extends Component {
  constructor (props) {
    super(props)
    const datapoint = props.cellParams.datapoint
    this.state = {
      display_value: datapoint.display_value ? datapoint.display_value : 'No Data'
    }
  }

  updateCell = value => {
    let display_value = 'No Data'
    if (value === '1') {
      display_value = 'Yes'
    } else if (value === '0') {
      display_value = 'No'
    }
    this.setState({display_value: display_value})
  }

  render = () => {
    const params = this.props.cellParams.params
    const datapoint = this.props.cellParams.datapoint
    const boolean_options = [
        { 'value': '0', 'title': 'No' },
        { 'value': '1', 'title': 'Yes' },
        { 'value': '', 'title': 'No Data' }
     ]

    return (
      <DropdownButton
        items={boolean_options}
        text={this.state.display_value}
        style='boolean-dropdown hollow'
        searchable={false}
        sendValue={value => {
          datapoint.value = value
          this.updateCell(value)
          this.props.cellParams.updateDatapoint(datapoint)
        }}
      />
    )
  }
}


export default BoolCell