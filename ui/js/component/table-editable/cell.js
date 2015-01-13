'use strict';

var _ = require('lodash');

module.exports = {
	replace : true,

	template: require('./cell.html'),

	data: function () {
		return {
			isEditing: false,
			isEditable: false
		};
	},

	ready: function() {
		console.log(this.$data.col.prop);
	},

	computed: {

		// format value for display
		cell: function (col) {
			var val = this.$parent[col.hasOwnProperty('prop') ? col.prop : col];

			if (col.hasOwnProperty('format') && _.isFunction(col.format)) {
				return col.format(val);
			}

			return val;
		},

		// format value for editing
		value: function (col) {
			var val = this.$parent[col.hasOwnProperty('prop') ? col.prop : col];

			return val;
		}

	}

};
