'use strict'

var _ = require('lodash')
var React = require('react/addons')
var cx = require('classnames')
var moment = require('moment')
var numeral = require('numeral')
var PropTypes = React.PropTypes
var InterfaceMixin = require('./../InterfaceMixin')
var SimpleDataTableColumn = require('./SimpleDataTableColumn')

var SimpleDataTableCell = React.createClass({
  displayName: 'SimpleDataTableCell',

  propTypes: {
    name: PropTypes.string,
    schema: PropTypes.object, // schema for this field
    field: PropTypes.object, // schema for this field
    row: PropTypes.object // the current data row which contains this cell
  },

  render: function render () {
    var field = this.props.field
    return React.createElement(
            'td',
            { className: 'ds-data-table-cell' },
            field.renderer(this.props.row[field.key], field, { moment: moment, numeral: numeral })
        )
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
              return React.createElement(SimpleDataTableCell, {
                name: column.props.name,
                schema: _this.props.schema.items.properties[column.props.name],
                field: _this.props.fields[column.props.name],
                row: row
              })
            })
        )
  }
})

module.exports = SimpleDataTable
