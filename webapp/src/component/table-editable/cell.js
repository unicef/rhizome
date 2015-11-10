'use strict'

var _ = require('lodash')

module.exports = {
  replace: true,

  template: require('./cell.html'),

  data: function () {
    return {
      previousValue: null, // save the previous value to compare with edited value
      isSaving: false, // whether the cell is in the process of saving right now
      isEditable: false, // whether the cell is editable
      isEditing: false, // whether the cell is currently being edited
      hasError: false
    }
  },

  created: function () {
    // set previous value
    this.previousValue = this.value || null
  },

  attached: function () {
    var self = this

    this.$el.addEventListener('mouseover', function () {
      self.$dispatch('tooltip-show', {
        el: self.$el,
        data: {
          text: self.hoverText,
          orientation: 'bottom'
        }
      })
    })

    this.$el.addEventListener('mouseout', function () {
      self.$dispatch('tooltip-hide', {
        el: self.$el
      })
    })
  },

  methods: {
    // switch editing mode
    toggleEditing: function (op) {
      if (this.$data.isEditable === true) {
        this.isEditing = op !== undefined ? op : !this.isEditing

        // set focus on input
        if (this.isEditing === true) {
          this.$el.getElementsByTagName('input')[0].focus()
        }
      }
    },

    // user has finished editing: update cell state
    submit: function () {
      var self = this

      self.hasError = false

      if (self.isSaving === false) {
        // only perform the save if value has changed
        if (self.value !== self.previousValue) {
          self.isSaving = true
          var passed = true
          var value = self.$data.value

          // validation
          if (self.validateValue !== undefined) {
            var validation = self.validateValue(value)
            if (validation.passed === true) {
              value = validation.value
            } else {
              // did not pass validation
              self.hasError = true
              // self.value = self.previousValue
              self.isSaving = false
              passed = false
            }
          }

          // submit value for saving
          if (passed === true && self.buildSubmitPromise !== undefined) {
            // TODO: validation of value

            var promise = self.buildSubmitPromise(value)
            promise.then(function (response) {
              // fulfilled
              if (self.withResponse) {
                self.withResponse(response)
              }
              // done saving
              self.previousValue = self.value
              self.isSaving = false
            }, function (error) {
              // or rejected
              if (self.withError) {
                self.withError(error)
              } else {
                console.log('Error', error)
              }

              // set to previous value
              self.hasError = true
              self.value = self.previousValue

              // done saving do not update value
              self.isSaving = false
            })
          }
        }

        // toggle editing mode
        self.toggleEditing(false)
      }
    }
  },

  computed: {
    formatted: function () {
      if (this.value === undefined || this.value === null) {
        return ''
      } else {
        // format according to attached method if it exists
        return this.format ? this.format(this.value) : this.value
      }
    },

    missing: function () {
      return _.isNull(this.value)
    },

    hoverText: function () {
      if (this.tooltip) {
        return this.tooltip
      } else if (_.isNull(this.value)) {
        return 'Missing value'
      } else {
        return this.value
      }
    }
  },

  filters: {
    // validate value
    validator: {
      write: function (val) {
        if (_.isString(val)) { // string
          if (val.length === 0) { val = null }
        } else if (_.isNumber(val)) { // number

        } else if (_.isNaN(val)) { // NaN
          val = null
        }

        // custom validation
        if (this.validate) {
          val = this.validate(val)
        }

        // update value
        return val
      }
    }
  }

}
