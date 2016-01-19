import _ from 'lodash'
import Reflux from 'reflux'
import d3 from 'd3'
import api from 'data/api'

let newCounter = function () {
  return {
    'complete': 0,
    'total': 0
  }
}

let TableEditaleStore = Reflux.createStore({
  listenables: [require('actions/TableEditableActions')],

  data: {
    table: {
      rows: [],
      columns: []
    },
    total: newCounter(),
    byRow: [],
    byColumn: [],
    processed: false
  },

  _updateStats: function () {
    if (this.data.table.rows.length > 0) {
      this.data.total = newCounter()
      _.forEach(this.data.table.rows, (row, rowIndex) => {
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
  },

  getInitialState: function () {
    return this.data
  },

  onInit: function (data, indicatorSet, indicatorMap, locationMap, locations, campaignId) {
    this.data.processed = false
    this.trigger(this.data)

    // define columns
    let columns = [{
      header: 'Indicator',
      type: 'label',
      headerClasses: 'medium-3'
    }]

    // add location names as columns
    _.forEach(locations, locationId => {
      columns.push({
        header: locationMap[locationId].name,
        type: 'value',
        key: locationId,
        children: null
      })
    })

    // cell formatter
    var numericFormatter = function (v) {
      return (isNaN(v) || _.isNull(v)) ? v : d3.format('n')(v)
    }

    // arrange datapoints into an object of indicators > locations
    var byIndicator = {}
    data.forEach(function (d) {
      if (!byIndicator[d.indicator_id]) { byIndicator[d.indicator_id] = {} }
      byIndicator[d.indicator_id][d.location_id] = d
    })

    // assemble data points into rows for table
    var rows = []

    _.each(indicatorSet.indicators, rowInfo => {
      var row = []
      if (rowInfo.type && rowInfo.type === 'section-header') { // section header row
        row.push({
          isEditable: false,
          type: 'label',
          value: rowInfo.title,
          class: 'section-header',
          colspan: columns.length
        })
      } else { // normal indicator row
        var indicator_id = rowInfo.id
        // add columns
        columns.forEach(column => {
          var cell = {
            isEditable: false,
            type: column.type
          }
          switch (column.type) {
            // editable value
            case 'value':
              cell.isEditable = true
              cell.format = numericFormatter
              cell.classes = 'numeric'
              cell.width = 80
              if (byIndicator[indicator_id] && byIndicator[indicator_id][column.key]) {
                cell.datapoint_id = byIndicator[indicator_id][column.key].datapoint_id
                cell.value = byIndicator[indicator_id][column.key].value
                cell.note = byIndicator[indicator_id][column.key].note
              } else {
                cell.datapoint_id = null
                cell.value = null
                cell.note = null
              }
              // tooltip
              if (locationMap[column.key] && indicatorMap[indicator_id]) {
                cell.tooltip = indicatorMap[indicator_id].name + ' value for ' + locationMap[column.key].name
              } else {
                cell.tooltip = null
              }
              // generate validation for values
              cell.validateValue = function (newVal) {
                var value, passed
                if (_.isNull(newVal)) {
                  value = null
                  passed = true
                } else {
                  value = parseFloat(newVal)
                  passed = !_.isNaN(value)
                }
                return { 'value': value, 'passed': passed }
              }

              // generate promise for submitting a new value to the API for saving
              cell.buildSubmitPromise = function (newVal) {
                var upsert_options = {
                  datapoint_id: cell.datapoint_id,
                  campaign_id: parseInt(campaignId, 10),
                  indicator_id: indicator_id,
                  location_id: column.key,
                  value: parseFloat(newVal)
                }
                return api.datapointUpsert(upsert_options)
              }

              // callback to specifically handle response
              cell.withResponse = function (response) {}

              // callback to handle error
              cell.withError = function (error) {
                console.log(error)
                if (error.msg && error.msg.message) { window.alert('Error: ' + error.msg.message) }
                cell.hasError = true
              }
              break

            // indicator name
            case 'label':
              cell.value = indicatorMap[indicator_id]
                ? indicatorMap[indicator_id].name
                : 'Missing info for indicator ' + indicator_id
              cell.classes = 'label'
              cell.width = 300
              break
          }
          row.push(cell)
        })
      } // end normal indicator row
      rows.push(row)
    })

    this.data.table.rows = rows
    this.data.table.columns = columns
    this._updateStats()

    this.data.processed = true
    this.trigger(this.data)
  },

  onUpdateStats: function () {
    this._updateStats()
    this.trigger(this.data)
  }
})

export default TableEditaleStore
