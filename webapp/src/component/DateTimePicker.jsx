'use strict';

var _        = require('lodash');
var d3       = require('d3');
var moment   = require('moment');
var React  = require('react');
var DateTimePicker = require('react-widgets/lib/DateTimePicker');

var DateRangePicker = React.createClass({

	propTypes: {
		start: React.PropTypes.object.isRequired,
		end: React.PropTypes.object.isRequired,
		sendValue : React.PropTypes.func.isRequired
	},

	getInitialState: function() {
		return {
			start: new Date(),
			end: new Date()
		}
	},

	handleDateChange: function(type, date, dateStr) {
		if (type == 'start') {
			this.setState({start: date});
		}
		else {
			this.setState({end: date});
		}
		this.props.sendValue(type, dateStr);
	},

	render() {
    var dateTimePicker = function(dateValue, type) {
      return (<DateTimePicker
          value={dateValue}
          time={false}
          format={'yyyy-MM-d'}
          onChange={this.handleDateChange.bind(this, type)}/>);
    };
		return (<div>
      {dateTimePicker(this.state.start, 'start')}
			<div class="centered">to</div>
      {dateTimePicker(this.state.end, 'end')}
	}
});

module.exports = DateRangePicker;

