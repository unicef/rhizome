'use strict';

var _ = require('lodash');

module.exports = {

	mixins: [
		require('./line')
	],

	ready: function () {
		console.info('year-over-year::ready');
		console.debug(this);
	},

	computed: {

		series: function () {
			console.info('year-over-year::series enter');

			if (this.empty) {
				console.info('year-over-year::series empty');
				return [];
			}

			var series = _.values(_.groupBy(this.datapoints, function (d) {
				return d.campaign.start_date.getFullYear();
			}));

			console.debug('year-over-year::series', series);
			console.info('year-over-year::series exit');
			return series;
		}

	}

};
