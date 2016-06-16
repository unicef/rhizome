import moment from 'moment'
import React from 'react'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'

var DateRangeSelect = React.createClass({
  propTypes: {
    start: React.PropTypes.object.isRequired,
    end: React.PropTypes.object.isRequired,
    start_date: React.PropTypes.object.isRequired,
    end_date: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    fromComponent: React.PropTypes.string.isRequired
  },

  getInitialState: function () {
    return {
      start: moment(this.props.start).format('YYYY-MM-DD'),
      end: moment(this.props.end).format('YYYY-MM-DD')
    }
  },

  componentWillReceiveProps: function (nextProps) {
    if (nextProps.fromComponent === 'ChartContainer') {
      this.setState({ start: nextProps.start, end: nextProps.end })
    }
  },

  handleDateChange: function (type, date, dateStr) {
    console.log('date', date)
    if (type === 'start') {
      this.setState({start: moment(date).format('YYYY-MM-DD')})
    } else {
      this.setState({end: moment(date).format('YYYY-MM-DD')})
    }
    this.props.sendValue(Object.assign({}, ))
  },

  render () {
    return (
      <div className='date-range-picker'>
        <DateTimePicker
          value={this.props.start_date}
          time={false}
          format={'YYYY-MM-DD'}
          onChange={date => this.handleDateChange('start', date)} />
        <span>to</span>
        <DateTimePicker
          value={this.props.end_date}
          time={false}
          format={'YYYY-MM-DD'}
          onChange={date => this.handleDateChange('end', date)} />
      </div>
    )
  }
})

export default DateRangeSelect
