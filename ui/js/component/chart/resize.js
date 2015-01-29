/* global window */

'use strict';

var dom = require('../../util/dom');
var log = require('../../util/log');

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
		log.debug('resize', 'ready');
		window.addEventListener('resize', this.onResize);
	},

	methods: {
		onResize: function () {
			log.debug('resize', 'onResize enter');

			if (!this.$el || !this.$el.parentElement) {
				log.debug('resize', 'onResize missing DOM elements');
				return;
			}

			var content = dom.contentArea(this.$el.parentElement);

			this.$set('width', content.width);
			this.$set('height', content.width / Number(this.aspect));

			this.$emit('invalidate-size');

			log.debug('resize', 'onResize exit');
		}
	},

	events: {
		'hook:attached': function () {
			log.debug('resize', 'hook:attached');
			this.onResize();
		}
	}
};
