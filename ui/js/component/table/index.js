'use strict';

var _ = require('lodash');

module.exports = {
	template: require('./template.html'),
	ready: function () {
		_.defaults(this.$data, {
			groupSize: 5
		});
	},
	filters: {
		isOdd: function (idx) {
			// It seems hack-ish to dig into the parent like this...
			return (idx % (this.$parent.$data.groupSize * 2)) < this.$parent.$data.groupSize;
		}
	}
};
