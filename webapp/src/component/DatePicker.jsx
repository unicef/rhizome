import React from 'react'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'

var DatePicker = React.createClass({
  propTypes: {
    date: React.PropTypes.object,
    sendValue: React.PropTypes.func.isRequired
  },

  getInitialState: function () {
    return {
      date: this.props.date
    }
  },

  handleDateChange: function (date, dateStr) {
    this.setState({date: date})
    this.props.sendValue(date, dateStr)
  },

  render () {
    var self = this
    return (<DateTimePicker
      value={self.state.date}
      time={false}
      format={'yyyy-MM-dd'}
      onChange={self.handleDateChange.bind(self)}/>)
  }
})

export default DatePicker

