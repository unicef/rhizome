/* global window */

'use strict';

var dom = require('../../util/dom');

module.exports = {
	replace : true,
	template: require('./template.html'),

	paramAttributes: [
		'data-orientation'
	],

	data: function () {
		return {
			orientation: 'top',
			show       : false,
			text       : null,

			top        : 0,
			right      : 0,
			bottom     : 0,
			left       : 0
		};
	},

	attached: function () {
		this.$el.parentElement.addEventListener('mouseover', this);
		this.$el.parentElement.addEventListener('mouseout', this);
		window.addEventListener('resize', this);
		this.$emit('tooltip-reposition');
	},

	methods: {
		handleEvent: function (evt) {
			console.debug('tooltip::handleEvent', evt.type, evt);
			var type = evt.type;

			switch (type) {
			case 'mouseover':
			case 'mouseout':
				this.show = (type === 'mouseover');
				break;

			case 'resize':
				this.$emit('tooltip-reposition');
				break;

			default:
				break;
			}

		}
	},

	events: {
		'tooltip-hide': function () {
			this.show = false;
		},

		'tooltip-reposition': function () {
			var offset = dom.offset(this.$el.parentElement);

			console.debug('tooltip::reposition offset', offset);

			switch (this.orientation) {
			case 'right':
				this.top    = offset.top + 'px';
				this.right  = 'auto';
				this.bottom = 'auto';
				this.left   = -offset.right + 'px';
				break;

			case 'bottom':
				this.top    = offset.bottom + 'px';
				this.right  = 'auto';
				this.bottom = 'auto';
				this.left   = offset.left + 'px';
				break;

			case 'left':
				this.top    = offset.top + 'px';
				this.right  = offset.left + 'px';
				this.bottom = 'auto';
				this.left   = 'auto';
				break;

			default:
				this.top    = 'auto';
				this.right  = 'auto';
				this.bottom = offset.top + 'px';
				this.left   = offset.left + 'px';
				break;
			}

			console.debug('tooltip::reposition position', this.top, this.right, this.bottom, this.left);
		},

		'tooltip-show': function () {
			this.show = true;
		},

		'tooltip-toggle': function () {
			this.show = !this.show;
		}
	}

};
