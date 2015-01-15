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
			return this.height - Number(this.marginTop) - Number(this.marginBottom);
		},

		contentTransform: function () {
			return 'translate(' + this.marginLeft + ',' + this.marginTop + ')';
		},

		contentWidth: function () {
			return this.width - Number(this.marginLeft) - Number(this.marginRight);
		}

	}

};
