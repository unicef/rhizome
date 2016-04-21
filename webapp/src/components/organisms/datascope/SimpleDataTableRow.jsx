import d3 from 'd3'
import React, {PropTypes} from 'react'
import EditableTableCell from 'components/atoms/EditableTableCell'
import TableCell from 'components/atoms/TableCell'
import IconButton from 'components/atoms/IconButton'

let SimpleDataTableRow = React.createClass({

  propTypes: {
    columns: PropTypes.array,
    row: PropTypes.array
  },

  _numberFormatter: function (v) {
    return (isNaN(v) || _.isNull(v)) ? v : d3.format('n')(v)
  },

  render: function () {
    const props = this.props
    const row = props.row
    const table_cells = React.Children.map(props.columns, column => {
      const cell_key = column.props.name
      const fields = props.fields
      const field = props.fields[cell_key]
      if (props.editable && cell_key !== 'location' && cell_key !== 'campaign') {

        return (
          <EditableTableCell
            field={field}
            row={row}
            value={row[cell_key].value}
            formatValue={this._numberFormatter}
            classes='numeric' />
        )
      } else {
        return (
          <TableCell
            field={field}
            row={row}
            value={row[cell_key].value}
            formatValue={this._numberFormatter}
            classes='numeric' />
        )
      }
    })

    const row_actions = props.rowAction ? (
      <td className='table-row-actions'>
        <IconButton
          className='clear-btn'
          onClick={() => props.rowAction(row.location_id)}
          text={'Remove ' + row.location}
          icon='fa-times-circle'/>
      </td>
     ) : null

    return (
      <tr>
        { row_actions }
        { table_cells }
      </tr>
    )
  }
})

export default SimpleDataTableRow
