'use strict';

module.exports = {

	paramAttributes: [
		'data-margin-top',
		'data-margin-right',
		'data-margin-bottom',
		'data-margin-left'
	],

	data: function () {
		return {
			marginTop   : 0,
			marginRight : 0,
			marginBottom: 0,
			marginLeft  : 0
		};
	},

	computed: {

		contentHeight: function () {
			if (!this.height) {
				return 0;
			}

			var h = this.height;

			if (this.marginTop) {
				h -= Number(this.marginTop);
			}

			if (this.marginBottom) {
				h -= Number(this.marginBottom);
			}

			return h;
		},

		contentTransform: function () {
			var x = this.marginLeft || 0;
			var y = this.marginTop || 0;

			return 'translate(' + x + ',' + y + ')';
		},

		contentWidth: function () {
			if (!this.width) {
				return 0;
			}

			var w = this.width;

			if (this.marginLeft) {
				w -= Number(this.marginLeft);
			}

			if (this.marginRight) {
				w -= Number(this.marginRight);
			}

			return w;
		}

	}

};
