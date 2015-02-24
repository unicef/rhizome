'use strict';

module.exports = {

	replace : true,
	template: require('./item.html'),

	data: function () {
		return {
			padding  : 17,
			level    : 0,
			open     : false,
			selected : false,
			children : []
		};
	},

	computed: {

		hasChildren: function () {
			return this.children && this.children.length > 0;
		},

		indent: function () {
			return (this.padding * this.level) + 'px';
		}

	},

	methods: {

		onClick: function () {
			this.$dispatch('dropdown-item-toggle', this);
		},

		toggleFolder: function (e) {
			this.open = !this.open;
			e.stopPropagation();
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
