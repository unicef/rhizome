'use strict';

var moment = require('moment');
var React = require('react');
var DateTimePicker = require('react-widgets/lib/DateTimePicker');

var DatePicker = React.createClass({

  propTypes: {
    date: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  getInitialState: function () {
    return {
      date: new Date()
    }
  },

  handleDateChange: function (date, dateStr) {
    this.setState({date: date});
    this.props.sendValue(date, dateStr);
  },

  render() {
    var self = this;
    return (<DateTimePicker
      value={self.state.date}
      time={false}
      format={'yyyy-MM-dd'}
      onChange={self.handleDateChange.bind(self)}/>);
  }
});

module.exports = DatePicker;

