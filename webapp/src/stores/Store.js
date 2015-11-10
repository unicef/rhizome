'use strict'

var _ = require('lodash')
var EventEmitter = require('events').EventEmitter

var CHANGE_EVENT = 'change'

module.exports = _.assign({}, EventEmitter.prototype, {
  CHANGE_EVENT: CHANGE_EVENT,

  emitChange: function () {
    this.emit(CHANGE_EVENT)
  },

  addChangeListener: function (cb) {
    this.on(CHANGE_EVENT, cb)
  },

  removeChangeListener: function (cb) {
    this.removeListener(CHANGE_EVENT, cb)
  }
})
