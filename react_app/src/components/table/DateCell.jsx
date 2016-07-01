import moment from 'moment'
import React, {Component} from 'react'
import DropdownButton from 'components/button/DropdownButton'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'

class DateCell extends Component {
  constructor (props) {
    super(props)
    const date = moment(props.datapoint.data_date).toDate()
    this.state = {
      display_date: date
    }
  }

  _updateDate = date => {
    const datapoints = this.props.datapoint
    const new_date = moment(date).format('YYYY-MM-DD')
    console.log('new_date', new_date)

    // this.props.updateDatapoint
    this.setState({display_date: date})
    if (datapoint.id) {}

  }

  render = () => {
    return (
      <DateTimePicker
        value={this.state.display_date}
        time={false}
        format={'YYYY-MM-DD'}
        onChange={this._updateDate} />
    )
  }
}


export default DateCell