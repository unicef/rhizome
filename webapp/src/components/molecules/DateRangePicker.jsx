import React from 'react'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'

var DateRangePicker = React.createClass({
  propTypes: {
    start: React.PropTypes.object.isRequired,
    end: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    fromComponent: React.PropTypes.string.isRequired
  },

  getInitialState: function () {
    return {
      start: this.props.start,
      end: this.props.end
    }
  },

  componentWillReceiveProps: function (nextProps) {
    if (nextProps.fromComponent === 'DataExplorer') {
      this.setState({
        start: nextProps.start,
        end: nextProps.end
      })
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
    return (
      <div className='date-range-picker'>
        <DateTimePicker
          value={this.state.start}
          time={false}
          format={'yyyy-MM-dd'}
          onChange={this.handleDateChange.bind(this, 'start')} />
        <span>to</span>
        <DateTimePicker
          value={this.state.end}
          time={false}
          format={'yyyy-MM-dd'}
          onChange={this.handleDateChange.bind(this, 'end')} />
      </div>
    )
  }
})

export default DateRangePicker
