'use strict';

var _   = require('lodash');

var dom = require('../../util/dom');

module.exports = {
	template: require('./template.html'),

	inherit : true,
	replace : true,

	paramAttributes: [
		'data-orientation'
	],

	data: function () {
		return {
			orientation: 'top',
			show       : false,

			top        : 0,
			right      : 0,
			bottom     : 0,
			left       : 0
		};
	},

	ready: function () {
		console.debug('tooltip::ready');
		this.$log();
		this.$root.$on('tooltip-show', this.showTooltip);
		this.$root.$on('tooltip-hide', this.hideTooltip);
	},

	methods: {
		reposition: function () {
			if (!this._parentEl) {
				return;
			}

			var offset = dom.documentOffset(this._parentEl);
			var doc = this._parentEl.ownerDocument.documentElement;

			console.debug('tooltip::reposition offset', offset);

			switch (this.orientation) {
			case 'right':
				this.top    = offset.top + 'px';
				this.right  = 'auto';
				this.bottom = 'auto';
				this.left   = offset.right + 'px';
				break;

			case 'bottom':
				this.top    = offset.bottom + 'px';
				this.right  = 'auto';
				this.bottom = 'auto';
				this.left   = offset.left + 'px';
				break;

			case 'left':
				this.top    = offset.top + 'px';
				this.right  = (doc.clientWidth - offset.left) + 'px';
				this.bottom = 'auto';
				this.left   = 'auto';
				break;

			default:
				this.top    = 'auto';
				this.right  = 'auto';
				this.bottom = (doc.clientHeight - offset.top) + 'px';
				this.left   = offset.left + 'px';
				break;
			}

			console.debug('tooltip::reposition position', this.top, this.right, this.bottom, this.left);
		},

		hideTooltip: function (options) {
			console.debug('tooltip::hide', options);
			if (this._parentEl === options.el) {
				this.show      = false;
				this._parentEl = null;

				window.removeEventListener('resize', this.reposition);
			}
		},

		showTooltip: function (options) {
			console.debug('tooltip::show', options);
			this._parentEl = options.el;

			var self = this;

			// FIXME: Crude version of Vue's mergeOptions...
			_.forOwn(options.data, function (v, k) {
				self.$set(k, v);
			});

			this.reposition();
			window.addEventListener('resize', this.reposition);
			this.show = true;
		}
	},

	partials: {
		'tooltip-default': '{{ text }}'
	}
};
