import _ from 'lodash'
import React from 'react'
import cx from 'classnames'

import InterfaceMixin from 'utilities/InterfaceMixin'
import TableHeaderCell from 'components/organisms/datascope/TableHeaderCell'
import SimpleDataTableCell from 'components/organisms/datascope/SimpleDataTableCell'

import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'

var TableToRefactor = React.createClass({
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
        emptyContent: React.PropTypes.node,
        // if true, puts emptyContent inside the tbody, otherwise shown instead of the table
        isEmptyContentInTable: React.PropTypes.bool,
        // sort up and down arrows
        sortIndicatorAscending: React.PropTypes.string,
        sortIndicatorDescending: React.PropTypes.string
    },
    getDefaultProps: function () {
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
        };
    },

    onClickColumnHeader: function (dataKey) {
        var isSortedOnColumn = dataKey === this.props.sortKey;
        var isSortAscending = (this.props.sortOrder || '').toLowerCase().indexOf('asc') === 0;

        // if not already sorted by this, sort descending by this
        // if already sorted descending by this, sort ascending
        // if already sorted ascending by this, remove sort
        var sortKey = !isSortedOnColumn || !isSortAscending ? dataKey : undefined;
        var sortOrder = !isSortedOnColumn ? 'descending' : !isSortAscending ? 'ascending' : undefined;
        //this.props.onChangeSort(sortKey, sortOrder);
        this.props.onChangeSort(sortKey, sortOrder);
    },

    render: function () {

      // if no data, and no "empty" message to show, hide table entirely
      var hasData = this.props.data && this.props.data.length;

      var children = this.props.children;
      children = _.isUndefined(children) ? [] : _.isArray(children) ? children : [children];
      var hasColumns = false;
      var columns = React.Children.map(this.props.children, function (child) {
          var isColumn = _.isFunction(child.type.implementsInterface) && child.type.implementsInterface('DataTableColumn');
          if (isColumn) hasColumns = true;
          return isColumn ? child : null;
      });

      if (!hasColumns) columns = _.map(this.props.orderedFields, function (field) {
          return React.createElement(SimpleDataTableColumn, { name: field.key });
      })

        var renderRow = _.partial(this.renderRow, columns)

      if (hasData || this.props.isEmptyContentInTable) {
        return (
          <table className={cx(['ds-data-table', { 'ds-data-table-sortable': this.props.sortable }])}>
              <thead>
                <tr>
                  { React.Children.map(columns, this.renderColumnHeader) }
                </tr>
              </thead>
          </table>
        )
      } else {
        return this.props.emptyContent
      }
    },
    //
    //   <tbody>
    //     { hasData ? this.props.data.map(renderRow) : this.props.emptyContent}
    //   </tbody>
    
    renderColumnHeader: function (column) {
        //console.log('sortKey', this.props.sortKey);
        var propsToPass = _.assign({}, _.clone(column.props), { // todo _.omit or _.pick
            field: this.props.fields[column.props.name],
            schema: this.props.schema.items.properties[column.props.name],
            onClick: this.props.sortable ? this.onClickColumnHeader.bind(this, column.props.name) : null,
            isSortedBy: column.props.name === this.props.sortKey,
            sortOrder: this.props.sortOrder,
            sortIndicatorAscending: this.props.sortIndicatorAscending,
            sortIndicatorDescending: this.props.sortIndicatorDescending
        });
        return React.createElement(TableHeaderCell, propsToPass);
    },
    renderRow: function (columns, row) {
        var _this = this;

        return React.createElement(
            'tr',
            null,
            React.Children.map(columns, function (column) {
                return React.createElement(SimpleDataTableCell, {
                    name: column.props.name,
                    schema: _this.props.schema.items.properties[column.props.name],
                    field: _this.props.fields[column.props.name],
                    row: row
                });
            })
        );
    }
});

export default TableToRefactor
