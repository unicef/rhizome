'use strict';

var _ = require('lodash');

module.exports = {
	template: require('./template.html'),

	ready: function () {
		_.defaults(this.$data, {
			groupSize: 5
		});
	},

	methods: {

	},

	components: {
		'uf-cell': require('./cell')
	}
};
