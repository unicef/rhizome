/* global window */
'use strict';

var dom = require('../../util/dom');

module.exports = {
	template: require('./template.html'),
	replace: true,

	paramAttributes: [
		'data-aspect',
		'data-margin-top',
		'data-margin-right',
		'data-margin-bottom',
		'data-margin-left'
	],

	data: function () {
		return {
			empty       : true,
			width       : 200,
			marginTop   : 0,
			marginRight : 0,
			marginBottom: 0,
			marginLeft  : 0
		};
	},

	attached: function () {
		window.addEventListener('resize', this);
		this.handleEvent();
	},

	filters: require('./filters'),
	directives: require('./directives'),

	computed: {
		contentWidth: function () {
			var left  = this.marginLeft || 0;
			var right = this.marginRight || 0;

			return this.width - left - right;
		},

		contentHeight: function () {
			var top    = this.marginTop || 0;
			var bottom = this.marginBottom || 0;

			return this.height - top - bottom;
		},

		height: function () {
			return this.width / (this.aspect || 1);
		},

		transform: function () {
			return 'translate(' + this.marginLeft + ',' + this.marginTop + ')';
		},

		empty: function () {
			if (this.values instanceof Array) {
				return this.values.length === 0;
			}

			return (typeof this.values === 'undefined') || this.values === null || this.values === '';
		}
	},

	methods: {
		handleEvent: function () {
			if (!this.$el || !this.$el.parentElement) {
				return;
			}

			var content = dom.contentArea(this.$el.parentElement);

			this.width = content.width;
			this.$broadcast('invalidateDisplay');
		}
	}
};
