'use strict';

module.exports = {
	replace : true,

	template: require('./item.html'),

	data: function () {
		return {
			open    : false,
			selected: false,
			pattern : ''
		};
	},

	computed: {
		hasChildren: function () {
			return this.children && this.children.length > 0;
		}
	},

	methods: {
		onClick: function () {
			this.selected = !this.selected;
		}
	},

	events: {
		'dropdown-select-all': function () {
			this.selected = true;
		},

		'dropdown-clear': function () {
			this.selected = false;
		},

		'dropdown-invert': function () {
			this.selected = !this.selected;
		}
	}

};
