'use strict';

var _ = require('lodash');

module.exports = {
	replace : true,

	template: require('./cell.html'),

	data: function() {
		return {
			previousValue: null, // save the previous value to compare with edited value
			isSaving: false, // whether the cell is in the process of saving right now
			isEditable: false, // whether the cell is editable
			isEditing: false // whether the cell is currently being edited
		};
	},

	created: function() {

		// set previous value
		this.previousValue = this.value || null;

	},

	methods: {

		// switch editing mode
		toggleEditing: function(op) {
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
			var self = this;

			if (self.isSaving === false) {

				// only perform the save if value has changed
				if (self.value !== self.previousValue) {

					self.isSaving = true;

					// submit value for saving
					if (self.buildSubmitPromise !== undefined) {

						var value = self.$data.value;
						// TODO: validation of value

						var promise = self.buildSubmitPromise(value);
						promise.then(function(response) {
							// fulfilled
							if (self.withResponse) {
								self.withResponse(response);
							}
							// done saving
							self.previousValue = self.value;
							self.isSaving = false;

						}, function(error) {
							// or rejected
							if (self.withError) {
								self.withError(error);
							} else {
								console.log('Error', error);
							}
							// done saving; do not update value
							self.isSaving = false;
						});

					}

				}
				
				// toggle editing mode
				self.toggleEditing(false);

			}

		}

	},

	computed: {

		formatted: function() {
			if (this.value === undefined || this.value === null) { 
				return ''; 
			}
			else {
				// format according to attached method if it exists
				return this.format ? this.format(this.value) : this.value;
			}
		},

		missing: function() {
			return _.isNull(this.value);
		},

		hoverText: function() {
			if (this.tooltip) {
				return this.tooltip;
			}
			else if (_.isNull(this.value)) {
				return 'Missing value';
			} else {
				return this.value;
			}
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
