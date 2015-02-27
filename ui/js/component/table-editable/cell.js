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

	created: function() {

		// set previous value
		this.previousValue = this.value || null;

	},

	attached: function () {
		var self = this;

		this.$el.addEventListener('mouseover', function () {
			self.$dispatch('tooltip-show', {
				el  : self.$el,
				data: {
					text: self.hoverText
				}
			});
		});

		this.$el.addEventListener('mouseout', function () {
			self.$dispatch('tooltip-hide', {
				el: self.$el
			});
		});
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

			// submit value for saving
			if (self.buildSubmitPromise !== undefined) {
				var value = self.$data.value;
				// TODO: compare new value to old?
				var promise = self.buildSubmitPromise(value);
				promise.done(function(response) {
					if (self.withResponse) {
						self.withResponse(response);
					}

				});

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
			if (_.isNull(this.value)) {
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
