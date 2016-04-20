import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import cx from 'classnames'
import InterfaceMixin from 'utilities/InterfaceMixin'
import TableHeaderCell from 'components/atoms/TableHeaderCell.jsx'
import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
import SimpleDataTableRow from 'components/organisms/datascope/SimpleDataTableRow'

import EditableTableCellStore from 'stores/EditableTableCellStore'

let SimpleDataTable = React.createClass({

  mixins: [
    InterfaceMixin('Datascope', 'DatascopeSort'),
    Reflux.connect(EditableTableCellStore, 'editedCell')
  ],

  propTypes: {
    data: React.PropTypes.array, // data displayed on the table, from Datascope
    schema: React.PropTypes.object, // data schema, from Datascope
    fields: React.PropTypes.object, // fields (display rules)
    orderedFields: React.PropTypes.array,
    query: React.PropTypes.object, // query (search, sort, filter)
    sortable: React.PropTypes.bool, // if true, can sort table by clicking header
    editable: React.PropTypes.bool, // if true, clicking on cells allows you to change the values
    sortKey: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]), // key for the column on which the data is sorted (eg. 'age')
    sortOrder: React.PropTypes.string, // order for the sort ('ascending' or 'descending')
    onChangeSort: React.PropTypes.func, // callback to call when user changes sort, passed implicitly by Datascope
    emptyContent: React.PropTypes.node, // if null, table will hide on no data // content to show in the table if there is no data
    isEmptyContentInTable: React.PropTypes.bool, // if true, puts emptyContent inside the tbody, otherwise shown instead of the table
    sortIndicatorAscending: React.PropTypes.string, // sort up and down arrows
    sortIndicatorDescending: React.PropTypes.string,
    children: React.PropTypes.array,
    sourceRow: React.PropTypes.array
  },

  getDefaultProps: function () {
    return {
      sortable: true,
      editable: false,
      emptyContent: <div className='ds-data-table-empty'>No results found</div>,
      isEmptyContentInTable: false,
      sortIndicatorAscending: ' ▲',
      sortIndicatorDescending: ' ▼'
    }
  },

  _withResponse: function (error) {
    if (error.msg && error.msg.message) { window.alert('Error: ' + error.msg.message) }
    console.log(error)
    this.hasError = true
  },

  _withError: function (error) {
    if (error.msg && error.msg.message) { window.alert('Error: ' + error.msg.message) }
    console.log(error)
    this.hasError = true
  },

  sortColumns: function (dataKey) {
    let isSortedOnColumn = dataKey === this.props.sortKey
    let isSortAscending = (this.props.sortOrder || '').toLowerCase().indexOf('asc') === 0
    // if not already sorted by this, sort descending by this
    // if already sorted descending by this, sort ascending
    // if already sorted ascending by this, remove sort
    let sortKey = !isSortedOnColumn || !isSortAscending ? dataKey : undefined
    let sortOrder = !isSortedOnColumn ? 'descending' : !isSortAscending ? 'ascending' : undefined
    this.props.onChangeSort(sortKey, sortOrder)
  },

  renderColumnHeader: function (column) {
    let propsToPass = _.assign({}, _.clone(column.props), { // todo _.omit or _.pick
      field: this.props.fields[column.props.name],
      schema: this.props.schema.items.properties[column.props.name],
      onClick: this.props.sortable ? this.sortColumns.bind(this, column.props.name) : null,
      isSortedBy: column.props.name === this.props.sortKey,
      sortOrder: this.props.sortOrder,
      sortIndicatorAscending: this.props.sortIndicatorAscending,
      sortIndicatorDescending: this.props.sortIndicatorDescending
    })
    return <TableHeaderCell {...propsToPass} />
  },

  render: function () {
    const props = this.props
    // if no data, and no "empty" message to show, hide table entirely
    let hasData = props.data && props.data.length
    if (!hasData && _.isNull(props.emptyContent)) return null

    let children = props.children
    children = _.isUndefined(children) ? [] : _.isArray(children) ? children : [children]
    let hasColumns = false
    let columns = React.Children.map(props.children, function (child) {
      let isColumn = _.isFunction(child.type.implementsInterface) && child.type.implementsInterface('DataTableColumn')
      if (isColumn) hasColumns = true
      return isColumn ? child : null
    })
    if (!hasColumns) {
      columns = props.orderedFields.map(field => React.createElement(SimpleDataTableColumn, { name: field.key }))
    }
    // build teh source footer by reversing the schema anad creating a row //
    // of cells so we can match indicator data with the source //
    let sourceDataObject = props.schema.items.properties
    let sourceDataFields = Object.keys(sourceDataObject).reverse()
    let sourceRow = _.map(sourceDataFields, function (field) {
      return <td>{sourceDataObject[field].source_name}</td>
    })

    if (hasData || props.isEmptyContentInTable) {
      return (
      <table className={cx(['ds-data-table', { 'ds-data-table-sortable': props.sortable }])}>
        <thead>
          <tr>
            {props.rowAction ? <th></th> : null }
            {React.Children.map(columns, this.renderColumnHeader)}
          </tr>
        </thead>
        <tbody>
          {hasData ? props.data.map(row => {
            return <SimpleDataTableRow row={row} columns={columns} {...props}/>
          }) : props.emptyContent}
        </tbody>
        <tfoot>
          {props.rowAction ? <td></td> : null }
          {sourceRow}
        </tfoot>
      </table>
      )
    } else {
      return props.emptyContent
    }
  }
})

export default SimpleDataTable
