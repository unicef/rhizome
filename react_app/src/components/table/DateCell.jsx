import moment from 'moment'
import React, {Component} from 'react'
import DropdownButton from 'components/button/DropdownButton'

class DateCell extends Component {
  render = () => {
    const params = this.props.cellParams
    const datapoint = this.props.cellParams.datapoint
    // const boolean_options = [
    //     { 'value': '0', 'title': 'No' },
    //     { 'value': '1', 'title': 'Yes' },
    //     { 'value': '', 'title': 'No Data' }
    //  ]
    console.log('this.props', this.props)
    console.log('params', params)
    console.log('datapoint', datapoint)
    const unformatted_date = params.value
    console.log('unformatted_date', unformatted_date)
    const date = moment(unformatted_date).format('YYYY-MM-DD')
    console.log('date', date)
    return (
      <div>{date}</div>
    )
  }
}


export default DateCell