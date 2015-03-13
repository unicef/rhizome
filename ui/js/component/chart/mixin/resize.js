/* global window */

'use strict';

var d3      = require('d3');

var browser = require('util/browser');
var dom     = require('util/dom');

module.exports = {
	paramAttributes: [
		'data-aspect'
	],

	data: function () {
		return {
			aspect: 1,
			height: 0,
			width : 0
		};
	},

	ready: function () {
		window.addEventListener('resize', this.onResize);

		if (browser.isIE()) {
			var svg = d3.select(this.$el.getElementsByTagName('svg')[0]);

			svg.attr({
				'width' : this.width,
				'height': this.height,
			});

			var self = this;

			this.$watch('width', function () {
				svg.attr('width', self.width);
			});

			this.$watch('height', function () {
				svg.attr('height', self.height);
			});
		}
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
