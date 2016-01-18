import React from 'react'
import _ from 'lodash'
import d3 from 'd3'
import api from '../../data/api'

var TableEditale = React.createClass({
  propTypes: {
    data: React.PropTypes.object,
    loaded: React.PropTypes.bool,
    indicatorSet: React.PropTypes.object,
    indicatorMap: React.PropTypes.object,
    locationMap: React.PropTypes.object,
    locations: React.PropTypes.array,
    campaignId: React.PropTypes.string
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return !_.isEqual(nextProps.loaded, this.props.loaded)
  },

  _buildData: function () {
    // define columns
    let columns = [{
      header: 'Indicator',
      type: 'label',
      headerClasses: 'medium-3'
    }]

    // add location names as columns
    _.forEach(this.props.locations, locationId => {
      columns.push({
        header: this.props.locationMap[locationId].name,
        type: 'value',
        key: locationId,
        children: null
      })
    })

    // cell formatters
    var numericFormatter = function (v) {
      return (isNaN(v) || _.isNull(v)) ? v : d3.format('n')(v)
    }

    // arrange datapoints into an object of indicators > locations
    var byIndicator = {}
    this.props.data.forEach(function (d) {
      if (!byIndicator[d.indicator_id]) { byIndicator[d.indicator_id] = {} }
      byIndicator[d.indicator_id][d.location_id] = d
    })

    // assemble data points into rows for table
    var rows = []

    _.each(this.props.indicatorSet.indicators, rowInfo => {
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
              if (this.props.locationMap[column.key] && this.props.indicatorMap[indicator_id]) {
                cell.tooltip = this.props.indicatorMap[indicator_id].name + ' value for ' + this.props.locationMap[column.key].name
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
                  campaign_id: parseInt(this.props.campaignId, 10),
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
              cell.value = this.props.indicatorMap[indicator_id]
                ? this.props.indicatorMap[indicator_id].name
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

    return {rows: rows, columns: columns}
  },

  _buildTable: function (data) {
    let tableContent = (
      <div>
        <h5>
        data
        </h5>
      </div>
    )
    return tableContent
  },

  render: function () {
    if (!this.props.loaded) {
      return (<div className='empty'>Use the options above to load a data entry form.</div>)
    } else if (this.props.indicatorSet.indicators.length < 1) {
      return (<div className='empty'>Use the options above to load a data entry form.</div>)
    } else {
      return this._buildTable(this._buildData())
    }
  }
})

export default TableEditale
