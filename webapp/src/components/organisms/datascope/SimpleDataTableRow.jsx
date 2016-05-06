import d3 from 'd3'
import React, {PropTypes} from 'react'
import EditableTableCell from 'components/organisms/datascope/EditableTableCell'
import TableCell from 'components/organisms/datascope/TableCell'
import IconButton from 'components/button/IconButton'

let SimpleDataTableRow = React.createClass({

  propTypes: {
    columns: PropTypes.array,
    row: PropTypes.array
  },

  _numberFormatter: function (v) {
    return (isNaN(v) || _.isNull(v)) ? v : d3.format('n')(v)
  },

  handleClick: function (rowLocation_id) {
    this.props.rowAction(rowLocation_id)
    this.removeTooltip()
  },

  removeTooltip: function () {
    let tooltipCollection = document.getElementsByClassName('tooltip')
    for (var idx = 0; idx < tooltipCollection.length; idx++) {
      tooltipCollection[idx].remove()
    }
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
          onClick={() => this.handleClick(row.location_id)}
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
