'use strict';

module.exports = {

	replace : true,
	template: require('./template.html'),

	paramAttributes = [
		'data-text'
	],

	data: function () {
		return {
			orientation: 'top',
			show       : false,
			text       : null
		};
	},

	computed: {

		bottom: function () {
			if (this.orientation !== 'top') {
				return 'auto';
			}
		},

		left: function () {
			if (this.orientation === 'left') {
				return 'auto';
			}
		},

		right: function () {
			if (this.orientation !== 'left') {
				return 'auto';
			}
		},

		top: function () {
			if (this.orientation === 'top') {
				return 'auto';
			}
		},

	}

};
