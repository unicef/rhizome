import React from 'react'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'

var DateRangePicker = React.createClass({
  propTypes: {
    start: React.PropTypes.object.isRequired,
    end: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    text: React.PropTypes.string
  },

  getInitialState: function () {
    return {
      start: new Date(),
      end: new Date()
    }
  },

  handleDateChange: function (type, date, dateStr) {
    if (type === 'start') {
      this.setState({start: date})
    } else {
      this.setState({end: date})
    }
    this.props.sendValue(type, dateStr)
  },

  render () {
    var self = this
    var dateTimePicker = function (dateValue, type) {
      return (<DateTimePicker
        value={dateValue}
        time={false}
        format={'yyyy-MM-dd'}
        onChange={self.handleDateChange.bind(this, type)}/>)
    }
    return (
        <div>
        {dateTimePicker(this.state.start, 'start')}
            <div className='centered'>{this.props.text}</div>
        {dateTimePicker(this.state.end, 'end')}
        </div>
    )
  }
})

export default DateRangePicker
