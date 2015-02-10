/* global window */

'use strict';

var dom = require('util/dom');

module.exports = {
	paramAttributes: [
		'data-aspect'
	],

	data: function () {
		return {
			aspect: 1

		};
	},

	ready: function () {
		window.addEventListener('resize', this.onResize);
	},

	computed: {
		viewBox: function () {
			return '0 0 ' + this.width + ' ' + this.height;
		}
	},

	methods: {
		onResize: function () {
			if (!this.$el || !this.$el.parentElement) {
				return;
			}

			var content = dom.contentArea(this.$el.parentElement);

			this.$set('width', content.width);

			if (this.aspect) {
				this.$set('height', content.width / Number(this.aspect));
			}

			this.$emit('invalidate-size');
		}
	},

	events: {
		'hook:attached': function () {
			this.onResize();
		}
	}
};
