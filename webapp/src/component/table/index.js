'use strict'

import _ from 'lodash'
import Vue from 'vue'

module.exports = {
  template: require('./template.html'),
  ready: function () {
    _.defaults(this.$data, {
      groupSize: 5
    })
  },
  filters: {
    isOdd: function (idx) {
      // It seems hack-ish to dig into the parent like this...
      return (idx % (this.$parent.$data.groupSize * 2)) < this.$parent.$data.groupSize
    },
    header: function (col) {
      if (col.hasOwnProperty('display')) {
        return _.isFunction(col.display) ? col.display(col) : col.display
      }

      return Vue.filter('capitalize')(col)
    },
    cell: function (col) {
      var val = this.$parent[col.hasOwnProperty('prop') ? col.prop : col]

      if (col.hasOwnProperty('format') && _.isFunction(col.format)) {
        return col.format(val)
      }

      return val
    },
    classes: function (col) {
      return String(col.classes)
    }
  }
}
