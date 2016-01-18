import _ from 'lodash'
import Reflux from 'reflux'

let newCounter = function () {
  return {
    'complete': 0,
    'total': 0
  }
}

let TableEditaleStore = Reflux.createStore({
  listenables: [require('actions/TableEditableActions')],

  data: {
    total: newCounter(),
    byRow: [],
    byColumn: []
  },

  getInitialState: function () {
    return this.data
  },

  onUpdateStats: function (data) {
    if (data.rows.length > 0) {
      _.forEach(data.rows, (row, rowIndex) => {
        if (this.data.byRow[rowIndex] === undefined) {
          this.data.byRow[rowIndex] = newCounter()
        }

        _.forEach(row, (cell, colIndex) => {
          if (this.data.byColumn[colIndex] === undefined) {
            this.data.byColumn[colIndex] = newCounter()
          }

          if (cell.isEditable) {
            this.data.total.total ++
            this.data.byRow[rowIndex].total ++
            this.data.byColumn[colIndex].total ++

            if (!_.isNull(cell.value)) {
              this.data.total.complete ++
              this.data.byRow[rowIndex].complete ++
              this.data.byColumn[colIndex].complete ++
            }
          }
        })
      })
    }
    this.trigger(this.data)
  }
})

export default TableEditaleStore
