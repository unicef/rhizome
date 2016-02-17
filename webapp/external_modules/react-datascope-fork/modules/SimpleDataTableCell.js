import React from 'react/addons'
import moment from 'moment'
import numeral from 'numeral'

let SimpleDataTableCell = React.createClass({
  displayName: 'SimpleDataTableCell',

  propTypes: {
    name: React.PropTypes.string,
    schema: React.PropTypes.object, // schema for this field
    field: React.PropTypes.object, // schema for this field
    row: React.PropTypes.object // the current data row which contains this cell
  },

  render: function () {
    var field = this.props.field
    return React.createElement(
      'td',
      { className: 'ds-data-table-cell' },
      field.renderer(this.props.row[field.key], field, { moment: moment, numeral: numeral })
    )
  }
})

export default SimpleDataTableCell
