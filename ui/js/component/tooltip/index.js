'use strict';

module.exports = {
	replace : true,
	template: require('./template.html'),

	paramAttributes: [
		'data-orientation'
	],

	data: function () {
		return {
			orientation: 'top',
			show       : false,
			text       : null
		};
	},

	events: {
		'tooltip-hide': function () {
			this.show = false;
		},

		'tooltip-show': function () {
			this.show = true;
		},

		'tooltip-toggle': function () {
			this.show = !this.show;
		}
	}
};
