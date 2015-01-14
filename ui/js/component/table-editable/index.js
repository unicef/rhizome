'use strict';

var _ = require('lodash');
var Vue = require('vue');

module.exports = {
	template: require('./template.html'),
	ready: function () {
		_.defaults(this.$data, {
			groupSize: 5
		});
	},
	methods: {

		switchMode: function () {

		}

	},
	filters: {

		isOdd: function (idx) {
			// It seems hack-ish to dig into the parent like this...
			return (idx % (this.$parent.$data.groupSize * 2)) < this.$parent.$data.groupSize;
		},

		header: function (col) {
			if (col.hasOwnProperty('display')) {
				return _.isFunction(col.display) ? col.display(col) : col.display;
			}

			return Vue.filter('capitalize')(col);
		},

		classes: function (col) {
			return String(col.classes);
		}
	},

	components: {
		'cell': require('./cell')
	}
};
