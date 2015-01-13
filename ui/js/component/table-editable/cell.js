'use strict';

var _ = require('lodash');

module.exports = {
	replace : true,

	template: require('./cell.html'),

	data: function() {
		return {
			isEditable: false,
			isEditing: false
		};
	},

	methods: {

		// switch editing mode
		toggleEditing: function(op) {
			console.log('toggle', op);
			if (this.$data.isEditable === true) {
				this.isEditing = op !== undefined ? op : !this.isEditing;

				// set focus on input
				if (this.isEditing === true) {
					this.$el.getElementsByTagName('input')[0].focus();
				}
			}
		},

		// user has finished editing: update cell state
		submit: function() {
			console.log('submit');

			// TO DO: submit value for saving (here?)
			
			// toggle editing mode
			this.toggleEditing(false);
		}

	},

	computed: {

		formatted: function() {
			if (!this.value) { return ''; }
			else {
				// format according to attached method if it exists
				return this.format ? this.format(this.value) : this.value;
			}
		},

		missing: function() {
			return _.isNull(this.value);
		}

	},

	filters: {

		// validate value
		validator: { 

			write: function(val) {

				// string
				if (_.isString(val)) {
					if (val.length === 0) { val = null; }
				} 
				// number
				else if (_.isNumber(val)) {

				} 
				// NaN
				else if (_.isNaN(val)) {
					val = null;
				}

				// custom validation
				if (this.validate) {
					val = this.validate(val);
				}

				// update value
				return val;

			}

		}

	}

};
