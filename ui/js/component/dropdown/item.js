'use strict';

module.exports = {

	replace : true,
	template: require('./item.html'),

	data: function () {
		return {
			open    : false,
			selected: false,
			children: []
		};
	},

	computed: {

		hasChildren: function () {
			return this.children && this.children.length > 0;
		},

	},

	methods: {

		toggle: function () {
			this.selected = !this.selected;
			this.$dispatch('dropdown-item-toggle', this);
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
