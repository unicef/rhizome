/* global window */

'use strict';

var Vue = require('vue');

var dom = require('util/dom');

module.exports = {
	replace  : true,
	template : require('./template.html'),

	paramAttributes : ['data-change-event'],

	data : function () {
		return {
			items       : [],
			open        : false,
			marginLeft  : 0,
			maxHeight   : 'none',
			orientation : 'center',
			changeEvent : 'menu-item-click'
		};
	},

	ready : function () {
		window.addEventListener('resize', this.onResize);
	},

	methods : {

		toggleMenu : function (event) {
			event.stopPropagation();

			this.open = !this.open;
			window.addEventListener('click', this.onClick);

			Vue.nextTick(this.onResize);
		},

		onClick : function () {
			this.open = false;
		},

		onItemClick : function (event, data) {
			event.preventDefault();
			this.$dispatch(this.changeEvent, data);
			this.open = false;
		},

		onResize : function () {
			var el     = dom.dimensions(this.$el);
			var menu   = dom.dimensions(this.$$.menu, true);
			var offset = dom.viewportOffset(this.$el);

			this.maxHeight = window.innerHeight - offset.top;

			var rightEdge = offset.left + (el.width / 2) + (menu.width / 2);
			var leftEdge  = offset.left + (el.width / 2) - (menu.width / 2);

			if (menu.width > window.innerWidth) {
				this.orientation = 'left';
				this.marginLeft  = 0;
			} else if (el.width >= menu.width) {
				this.orientation = 'center';
				this.marginLeft  = -menu.width / 2;
			} else if (leftEdge < 0) {
				this.orientation = 'left';
				this.marginLeft  = 0;
			} else if (rightEdge > window.innerWidth) {
				this.orientation = 'right';
				this.marginLeft  = 0;
			} else {
				this.orientation = 'center';
				this.marginLeft  = -menu.width / 2;
			}
		}

	}
};
