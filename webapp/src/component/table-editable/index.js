'use strict'

var _ = require('lodash')
var d3 = require('d3')

var formats = {
  percent: d3.format('%')
}

var scales = {
  completionClass: function (v) {
    if (v === 0) {
      return 'statusText-bad'
    } else if (v === 1) {
      return 'statusText-good'
    } else if (v > 0 && v < 1) {
      return 'statusText-okay'
    }
    return null
  }
}

module.exports = {
  template: require('./template.html'),

  ready: function () {
    _.defaults(this.$data, {
      groupSize: 5
    })

    // update the stats object when the rows data changes
    this.$watch('rows', this.updateStats, true, true)
  },

  methods: {
    // update table stats
    updateStats: function () {
      var self = this

      var newCounter = function () {
        return {
          'complete': 0,
          'total': 0
        }
      }

      var stats = {
        total: newCounter(),
        byRow: [],
        byColumn: []
      }

      if (self.rows.length > 0) {
        _.forEach(self.rows, function (row, rowIndex) {
          if (stats.byRow[rowIndex] === undefined) {
            stats.byRow[rowIndex] = newCounter()
          }

          _.forEach(row, function (cell, colIndex) {
            if (stats.byColumn[colIndex] === undefined) {
              stats.byColumn[colIndex] = newCounter()
            }

            if (cell.isEditable) {
              stats.total.total ++
              stats.byRow[rowIndex].total ++
              stats.byColumn[colIndex].total ++

              if (!_.isNull(cell.value)) {
                stats.total.complete ++
                stats.byRow[rowIndex].complete ++
                stats.byColumn[colIndex].complete ++
              }
            }
          }) // end column loop
        }) // end row loop
      }

      self.$set('stats', stats)
    }
  },

  filters: {
    percent: function (v) {
      return formats.percent(v)
    },

    completionClass: function (v) {
      return scales.completionClass(v)
    },

    getStat: function (obj, by, prop) {
      if (this.stats[by] && this.stats[by][this.$index] !== undefined && this.stats[by][this.$index][prop] !== undefined) {
        return this.stats[by][this.$index][prop]
      }
      return null
    },

    rowCompletionClass: function () {
      if (this.stats.byRow[this.$index] !== undefined) {
        return scales.completionClass(this.stats.byRow[this.$index].complete / this.stats.byRow[this.$index].total)
      }
      return null
    },

    colCompletionClass: function () {
      if (this.stats.byColumn[this.$index] !== undefined) {
        return scales.completionClass(this.stats.byColumn[this.$index].complete / this.stats.byColumn[this.$index].total)
      }
    }
  },

  components: {
    'uf-cell': require('./cell')
  }
}
