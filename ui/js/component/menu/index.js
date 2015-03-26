/* global window */

'use strict';

module.exports = {
	template : require('./template.html'),

	data : function () {
		return {
			items : [],
			open  : false,
			icon  : 'fa-bars',
		}
	},

	ready : function () {
		window.addEventListener('resize', this.onResize);
	},

	methods : {

		onResize : function () {

		}

	}
};
