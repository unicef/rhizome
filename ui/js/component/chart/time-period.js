'use strict';

var moment        = require('moment');

var parseDuration = require('../../util/date').parseDuration;

module.exports = {

	paramAttributes: [
		'data-date',
		'data-duration'
	],

	data: function () {
		return {
			date    : null,
			duration: null
		};
	},

	compiled: function () {
		if (typeof this.date === 'string') {
			this.date = moment(this.date, 'YYYY-MM-DD');
		}
	},

	computed: {

		interval: function () {
			if (!this.date && !this.duration) {
				return null;
			}

			var date;

			// Handle string dates, Date objects, numbers (milliseconds) and
			// missing values
			switch (typeof this.date) {
			case 'string':
				date = new moment(this.date, 'YYYY-MM-DD');
				break;

			case 'number':
			case 'undefined':
			case 'object':
				date = this.date ? moment(this.date) : moment();
				break;

			default:
				throw new Error('Unable to parse date value: ' + this.date);
			}

			var duration = parseDuration(this.duration);

			if (!duration) {
				return {
					campaign_end: date.format('YYYY-MM-DD')
				};
			}

			var start;
			var end;

			if (duration[0] < 0) {
				end   = date.format('YYYY-MM-DD');
				start = date.add.apply(date, duration).format('YYYY-MM-DD');
			} else {
				start = date.format('YYYY-MM-DD');
				end   = date.add.apply(date, duration).format('YYYY-MM-DD');
			}

			return {
				campaign_start: start,
				campaign_end  : end
			};
		}

	}

};
