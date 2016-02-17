import _ from 'lodash'
import React from 'react/addons'
import FixedDataTable from 'fixed-data-table'
import InterfaceMixin from './../InterfaceMixin'

let isColumnResizing

let DataTable = React.createClass({
  displayName: 'DataTable',

  mixins: [InterfaceMixin('Datascope', 'DatascopeSort')],

  propTypes: {
    // data displayed on the table
    data: React.PropTypes.array, // required
    // data schema
    schema: React.PropTypes.object, // required
    // key for the column which the data is sorted on (eg. 'age')
    sortKey: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]),
    // order for the sort ('ascending' or 'descending')
    sortOrder: React.PropTypes.string,
    // callback to call when user changes sort
    onChangeSort: React.PropTypes.func.isRequired
  },

  componentWillMount: function () {
    let _this = this

    this.width = 1000
    let fields = this.props.schema.fields
    this.setState({
      columnWidths: _.object(_.map(fields, function (field) {
        return [field.name, _this.width / fields.length]
      }))
    })
  },

  onColumnResizeEndCallback: function (newColumnWidth, dataKey) {
    let columnWidths = React.addons.update(this.state.columnWidths, _defineProperty({}, dataKey, { $set: newColumnWidth }))
    this.setState({ columnWidths: columnWidths })
    isColumnResizing = false
  },

  onClickColumnHeader: function (dataKey) {
    let isSortedOnColumn = dataKey === this.props.sortKey
    let isSortAscending = (this.props.sortOrder || '').toLowerCase().indexOf('asc') === 0

    // if not already sorted by this, sort descending
    // if already sorted descending by this, sort ascending
    // if already sorted ascending by this, remove sort
    let sortKey = !isSortedOnColumn || !isSortAscending ? dataKey : undefined
    let sortOrder = !isSortedOnColumn
    ? 'descending'
    : !isSortAscending
    ? 'ascending'
    : undefined
    this.props.onChangeSort(sortKey, sortOrder)
  },

  render: function () {
    let _this2 = this

    return React.createElement(
      'div',
      null,
      React.createElement(
        FixedDataTable.Table,
        {
          rowHeight: 50,
          rowGetter: function (i) {
            return _this2.props.data[i]
          },
          rowsCount: this.props.data.length,
          width: 1000,
          maxHeight: 5000,
          headerHeight: 50,
          isColumnResizing: isColumnResizing,
          onColumnResizeEndCallback: this.onColumnResizeEndCallback
        },
        _.map(this.props.schema.fields, function (field) {
          let isSortedOnColumn = field.name === _this2.props.sortKey
          let isSortAscending = (_this2.props.sortOrder || '').toLowerCase().indexOf('asc') === 0
          let sortArrow = isSortedOnColumn ? isSortAscending ? ' ▲' : ' ▼' : ''

          return React.createElement(FixedDataTable.Column, {
            label: field.title + sortArrow,
            dataKey: field.name,
            width: _this2.state.columnWidths[field.name] || 100,
            isResizable: true,
            headerRenderer: _this2.renderColumnHeader,
            sortKey: _this2.props.sortKey,
            key: field.name
          })
        })
      )
    )
  },

  renderColumnHeader: function (label, cellDataKey, columnData, rowData, width) {
    return React.createElement(
      'div',
      { onClick: this.onClickColumnHeader.bind(this, cellDataKey) },
      label
      )
  }
})

function _defineProperty (obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }) } else { obj[key] = value } return obj }

export default DataTable
