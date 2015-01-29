'use strict';

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
			text       : null
		};
	},

	attached: function () {
		this.$el.parentElement.addEventListener('mouseover', this);
		this.$el.parentElement.addEventListener('mouseout', this);
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

			default:
				break;
			}

		}
	},

	events: {
		'tooltip-hide': function () {
			this.show = false;
		},

		'tooltip-show': function () {
			this.show = true;
		},

		'tooltip-toggle': function () {
			this.show = !this.show;
		}
	}

};
