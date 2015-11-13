'use strict'

import React from 'react'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'

var DateRangePicker = React.createClass({
  propTypes: {
    start: React.PropTypes.object.isRequired,
    end: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
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
      var self1 = self
      return (<DateTimePicker
        value={dateValue}
        time={false}
        format={'yyyy-MM-dd'}
        onChange={self1.handleDateChange.bind(this, type)}/>)
    }
    return (
        <div>
        {dateTimePicker(this.state.start, 'start')}
            <div className='centered'>to</div>
        {dateTimePicker(this.state.end, 'end')}
        </div>
    )
  }
})

export default DateRangePicker
