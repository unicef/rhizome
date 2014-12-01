/* global window */
'use strict';

var dom = require('../../util/dom');

module.exports = {
	template: require('./template.html'),
	replace: true,

	paramAttributes: [
		'aspect'
	],

	data: function () {
		return {
			margin: {
				top   : 0,
				right : 0,
				bottom: 0,
				left  : 0
			},
			width: 200
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
			var left  = this.margin.left || 0;
			var right = this.margin.right || 0;

			return this.width - left - right;
		},

		contentHeight: function () {
			var top    = this.margin.top || 0;
			var bottom = this.margin.bottom || 0;

			return this.height - top - bottom;
		},

		height: function () {
			return this.width / (this.aspect || 1);
		},

		transform: function () {
			return 'translate(' + this.margin.left + ',' + this.margin.top + ')';
		}
	},

	methods: {
		handleEvent: function () {
			var content = dom.contentArea(this.$el.parentElement);

			this.width = content.width;
			this.$broadcast('invalidateDisplay');
		}
	}
};
