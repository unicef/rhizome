'use strict'

import api from 'data/api'
import _ from 'lodash'
import React from 'react'
import cx from 'classnames'
import d3 from 'd3'
// var moment = require('moment')
// var numeral = require('numeral')
var PropTypes = React.PropTypes
// var InterfaceMixin = require('../external/react-datascope/lib/InterfaceMixin.js')
// var SimpleDataTableColumn = require('./SimpleDataTableColumn')
import Cell from '02-molecules/TableEditableCell.jsx'

// No Idea what this does below //

Object.defineProperty(exports, '__esModule', {
  value: true
})
exports['default'] = InterfaceMixin

function InterfaceMixin () {
  for (var _len = arguments.length, interfaces = Array(_len), _key = 0; _key < _len; _key++) {
    interfaces[_key] = arguments[_key]
  }

  return {
    statics: {
      implementsInterface: function implementsInterface (name) {
        return interfaces.indexOf(name) >= 0
      }
    }
  }
}
// No Idea what that does above //

var SimpleDataTableColumn = React.createClass({
  displayName: 'SimpleDataTableColumn',

  mixins: [InterfaceMixin('DataTableColumn')],
  propTypes: {
    name: PropTypes.string, // field key
    title: PropTypes.string, // human-readable field name (to override schema)
    schema: PropTypes.object // schema for this column only (passed implicitly by SimpleDataTable)
  },
  render: function render () {
    throw new Error('SimpleDataTableColumn should never be rendered!')
  }
})

var TableHeaderCell = React.createClass({
  displayName: 'TableHeaderCell',

  propTypes: {
    schema: PropTypes.shape({
      name: PropTypes.string,
      title: PropTypes.string
    }), // schema for this field
    field: PropTypes.object,
    title: PropTypes.string, // to override schema title
    onClick: PropTypes.func, // usually the sort function
    isSortedBy: PropTypes.bool, // true if the table is sorted by this column
    sortIndicatorAscending: PropTypes.string,
    sortIndicatorDescending: PropTypes.string,
    sortOrder: PropTypes.string
  },
  getDefaultProps: function getDefaultProps () {
    return {
      onClick: null,
      sortIndicatorAscending: ' ▲',
      sortIndicatorDescending: ' ▼'
    }
  },
  _getTitle: function _getTitle () {
    return _.isUndefined(this.props.title) ? this.props.field.title : this.props.title
  },
  render: function render () {
    var isSortAscending = (this.props.sortOrder || '').toLowerCase().indexOf('asc') === 0
    var sortIndicator = this.props.isSortedBy ? isSortAscending ? this.props.sortIndicatorAscending : this.props.sortIndicatorDescending : ''

    return React.createElement(
            'th',
            { className: 'ds-data-table-col-head', onClick: this.props.onClick },
            React.createElement(
                'span',
                { className: 'ds-data-table-col-title' },
                this._getTitle()
            ),
            React.createElement(
                'span',
                { className: 'ds-data-table-sort-indicator' },
                sortIndicator
            )
        )
  }
})

var SimpleDataTable = React.createClass({
  displayName: 'SimpleDataTable',

  mixins: [InterfaceMixin('Datascope', 'DatascopeSort')],
  propTypes: {
        // data displayed on the table, from Datascope
    data: React.PropTypes.array,
    // data schema, from Datascope
    schema: React.PropTypes.object,
    // fields (display rules)
    fields: React.PropTypes.object,
    orderedFields: React.PropTypes.array,
    // query (search, sort, filter)
    query: React.PropTypes.object,

    // if true, can sort table by clicking header
    sortable: React.PropTypes.bool,
    // key for the column on which the data is sorted (eg. 'age')
    sortKey: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]),
    // order for the sort ('ascending' or 'descending')
    sortOrder: React.PropTypes.string,
    // callback to call when user changes sort, passed implicitly by Datascope
    onChangeSort: React.PropTypes.func,
    // content to show in the table if there is no data
    // if null, table will hide on no data
    emptyContent: PropTypes.node,
    // if true, puts emptyContent inside the tbody, otherwise shown instead of the table
    isEmptyContentInTable: PropTypes.bool,
    // sort up and down arrows
    sortIndicatorAscending: PropTypes.string,
    sortIndicatorDescending: PropTypes.string,
    children: PropTypes.array
  },
  getDefaultProps: function getDefaultProps () {
    return {
      sortable: true,
      emptyContent: React.createElement(
                'div',
                { className: 'ds-data-table-empty' },
                'No results found'
            ),
      isEmptyContentInTable: false,
      sortIndicatorAscending: ' ▲',
      sortIndicatorDescending: ' ▼'
    }
  },

  onClickColumnHeader: function onClickColumnHeader (dataKey) {
    var isSortedOnColumn = dataKey === this.props.sortKey
    var isSortAscending = (this.props.sortOrder || '').toLowerCase().indexOf('asc') === 0

    // if not already sorted by this, sort descending by this
    // if already sorted descending by this, sort ascending
    // if already sorted ascending by this, remove sort
    var sortKey = !isSortedOnColumn || !isSortAscending ? dataKey : undefined
    var sortOrder = !isSortedOnColumn ? 'descending' : !isSortAscending ? 'ascending' : undefined
    this.props.onChangeSort(sortKey, sortOrder)
  },

  render: function render () {
    // if no data, and no "empty" message to show, hide table entirely
    var hasData = this.props.data && this.props.data.length
    if (!hasData && _.isNull(this.props.emptyContent)) return null

    var children = this.props.children
    children = _.isUndefined(children) ? [] : _.isArray(children) ? children : [children]
    var hasColumns = false
    var columns = React.Children.map(this.props.children, function (child) {
      var isColumn = _.isFunction(child.type.implementsInterface) && child.type.implementsInterface('DataTableColumn')
      if (isColumn) hasColumns = true
      return isColumn ? child : null
    })

    if (!hasColumns) {
      columns = _.map(this.props.orderedFields, function (field) {
        return React.createElement(SimpleDataTableColumn, { name: field.key })
      })
    }

    var renderRow = _.partial(this.renderRow, columns)
    return hasData || this.props.isEmptyContentInTable ? React.createElement(
            'table',
            { className: cx(['ds-data-table', { 'ds-data-table-sortable': this.props.sortable }]) },
            React.createElement(
                'thead',
                null,
                React.createElement(
                    'tr',
                    null,
                    React.Children.map(columns, this.renderColumnHeader)
                )
            ),
            React.createElement(
                'tbody',
                null,
                hasData ? this.props.data.map(renderRow) : this.props.emptyContent
            )
        ) : this.props.emptyContent
  },

  renderColumnHeader: function renderColumnHeader (column) {
    var propsToPass = _.assign({}, _.clone(column.props), { // todo _.omit or _.pick
      field: this.props.fields[column.props.name],
      schema: this.props.schema.items.properties[column.props.name],
      onClick: this.props.sortable ? this.onClickColumnHeader.bind(this, column.props.name) : null,
      isSortedBy: column.props.name === this.props.sortKey,
      sortOrder: this.props.sortOrder,
      sortIndicatorAscending: this.props.sortIndicatorAscending,
      sortIndicatorDescending: this.props.sortIndicatorDescending
    })
    return React.createElement(TableHeaderCell, propsToPass)
  },
  renderRow: function renderRow (columns, row) {
    var _this = this

    return React.createElement(
            'tr',
            null,
            React.Children.map(columns, function (column) {
              return React.createElement(Cell, {
                item: {
                  name: column.props.name,
                  schema: _this.props.schema.items.properties[column.props.name],
                  field: _this.props.fields[column.props.name],
                  row: row,
                  value: row[column.props.name],
                  isEditable: true,
                  validateValue: _this._validateValue,
                  buildSubmitPromise: _this._buildSubmitPromise,
                  classes: 'numeric',
                  format: _this._numericFormatter,
                  tooltip: 'this is gonna work bro!!!!',
                  type: 'value',
                  withError: _this._withError,
                  withResponse: _this._withResponse
                }
              })
            })
        )
  },

  _withResponse: function (error) {
      var self = this
      console.log(error)
      if (error.msg && error.msg.message) { window.alert('Error: ' + error.msg.message) }
      self.hasError = true
    },

  _withError: function (error) {
      var self = this
      console.log(error)
      if (error.msg && error.msg.message) { window.alert('Error: ' + error.msg.message) }
      self.hasError = true
    },

  _numericFormatter: function (v) {
    return (isNaN(v) || _.isNull(v)) ? v : d3.format('n')(v)
  },

  _validateValue: function (newVal) {
    console.log('VALIDATING VALUEE!!!!!')
    var value, passed
    if (_.isNull(newVal)) {
      value = null
      passed = true
    } else {
      value = parseFloat(newVal)
      passed = !_.isNaN(value)
    }
    return { 'value': value, 'passed': passed }
  },

  _buildSubmitPromise: function (newVal) {
    console.log('Build Submit PRomise')
    var self = this
    var upsert_options = {
      datapoint_id: self.datapoint_id,
      campaign_id: 307, // parseInt(campaignId, 10),
      indicator_id: 22, // self.indicator_id,
      location_id: self.location_id,
      value: parseFloat(newVal)
    }
    return api.datapointUpsert(upsert_options)
  }

})
module.exports = SimpleDataTable
