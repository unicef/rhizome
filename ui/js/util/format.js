'use strict';

var moment = require('moment');

function timeAxis(value) {
	var m = moment(value);

	if (m.month() === 0) {
		return m.format('YYYY');
	}

	return m.format('MMM');
}

module.exports = {
	timeAxis: timeAxis
};
