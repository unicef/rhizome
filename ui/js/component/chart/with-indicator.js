'use strict';

var _ = require('lodash');
var api = require('../../data/api');

module.exports = {

	methods: {
		loadIndicator: function () {
			console.info('with-indicator::loadIndicator', 'watch');
			console.debug('with-indicator::loadIndicator', this.indicator);

			var self = this;

			if (!this.indicator) {
				return;
			}

			if (_.isNumber(this.indicator) || _.isString(this.indicator)) {
				api.indicators({ id: this.indicator })
					.then(function (data) {
						self.indicator = data.objects[0];
					}, this.dataError);
			} else {
				self.$emit('indicator-changed');
			}
		}
	},

	events: {
		'hook:created': 'loadIndicator'
	},

	watch: {
		'indicator': 'loadIndicator'
	}
};
