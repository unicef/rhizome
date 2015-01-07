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
			this.$dispatch('dropdown-item-selected', this);
		}
	},

	events: {

		'dropdown-select-all': function () {
			this.selected = true;
			this.$dispatch('dropdown-item-selected', this);
		},

		'dropdown-clear': function () {
			this.selected = false;
			this.$dispatch('dropdown-item-selected', this);
		},

		'dropdown-invert': 'toggle'

	},
};
