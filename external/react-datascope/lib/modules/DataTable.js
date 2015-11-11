'use strict';

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var _ = require('lodash');
var React = require('react/addons');
var FixedDataTable = require('fixed-data-table');
var InterfaceMixin = require('./../InterfaceMixin');

var isColumnResizing;

var DataTable = React.createClass({
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
    componentWillMount: function componentWillMount() {
        var _this = this;

        this.width = 1000;
        var fields = this.props.schema.fields;
        this.setState({
            columnWidths: _.object(_.map(fields, function (field) {
                return [field.name, _this.width / fields.length];
            }))
        });
    },

    onColumnResizeEndCallback: function onColumnResizeEndCallback(newColumnWidth, dataKey) {
        var columnWidths = React.addons.update(this.state.columnWidths, _defineProperty({}, dataKey, { $set: newColumnWidth }));
        this.setState({ columnWidths: columnWidths });
        isColumnResizing = false;
    },
    onClickColumnHeader: function onClickColumnHeader(dataKey) {
        var isSortedOnColumn = dataKey === this.props.sortKey,
            isSortAscending = (this.props.sortOrder || '').toLowerCase().indexOf('asc') === 0;

        // if not already sorted by this, sort descending
        // if already sorted descending by this, sort ascending
        // if already sorted ascending by this, remove sort
        var sortKey = !isSortedOnColumn || !isSortAscending ? dataKey : undefined;
        var sortOrder = !isSortedOnColumn ? 'descending' : !isSortAscending ? 'ascending' : undefined;
        this.props.onChangeSort(sortKey, sortOrder);
    },

    render: function render() {
        var _this2 = this;

        return React.createElement(
            'div',
            null,
            React.createElement(
                FixedDataTable.Table,
                {
                    rowHeight: 50,
                    rowGetter: function (i) {
                        return _this2.props.data[i];
                    },
                    rowsCount: this.props.data.length,
                    width: 1000,
                    maxHeight: 5000,
                    headerHeight: 50,
                    isColumnResizing: isColumnResizing,
                    onColumnResizeEndCallback: this.onColumnResizeEndCallback
                },
                _.map(this.props.schema.fields, function (field) {
                    var isSortedOnColumn = field.name === _this2.props.sortKey,
                        isSortAscending = (_this2.props.sortOrder || '').toLowerCase().indexOf('asc') === 0,
                        sortArrow = isSortedOnColumn
                          ? isSortAscending ? ' ▲' : ' ▼'
                          : ''

                    return React.createElement(FixedDataTable.Column, {
                        label: field.title + sortArrow,
                        dataKey: field.name,
                        width: _this2.state.columnWidths[field.name] || 100,
                        isResizable: true,
                        headerRenderer: _this2.renderColumnHeader,
                        sortKey: _this2.props.sortKey,
                        key: field.name
                    });
                })
            )
        );
    },
    renderColumnHeader: function renderColumnHeader(label, cellDataKey, columnData, rowData, width) {
        return React.createElement(
            'div',
            { onClick: this.onClickColumnHeader.bind(this, cellDataKey) },
            label
        );
    }
});

module.exports = DataTable;
