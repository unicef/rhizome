import React from 'react'
import moment from 'moment'
import numeral from 'numeral'

var SimpleDataTableCell = React.createClass({
    displayName: 'SimpleDataTableCell',

    propTypes: {
        name: React.PropTypes.string,
        schema: React.PropTypes.object, // schema for this field
        field: React.PropTypes.object, // schema for this field
        row: React.PropTypes.object // the current data row which contains this cell
    },
    render: function render() {
        var field = this.props.field;
        return React.createElement(
            'td',
            { className: 'ds-data-table-cell' },
            field.renderer(this.props.row[field.key], field, { moment: moment, numeral: numeral })
        );
    }
});
