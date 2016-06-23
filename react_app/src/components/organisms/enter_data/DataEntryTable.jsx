import _ from 'lodash'
import React from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import moment from 'moment'
import format from 'utilities/format'
import {reactCellRendererFactory} from 'ag-grid-react'
import IntegerCell from 'components/table/IntegerCell'
import BoolCell from 'components/table/BoolCell'
import PercentCell from 'components/table/PercentCell'

const DataEntryTable = (props) => {
  const datapoints = props.datapoints.including_missing
  const grouped_datapoints = _.groupBy(datapoints, 'location.id')
  const rows = _getRowData(grouped_datapoints)
  const columns = _getColumnData(grouped_datapoints, props.updateDatapoint, props.removeDatapoint)
  const grid_options = {
    rowHeight: 30,
    headerHeight: 48,
    colWidth: 150
  }

  return (
    <ResourceTable
      rowData={rows}
      columnDefs={columns}
      gridOptions={grid_options}
      resourcePath='datapoints'
      className='datapoint-table'
    />
  )
}

const _getRowData = grouped_datapoints => {
  const rows = grouped_datapoints ? _.map(grouped_datapoints, datapoint_group => {
    const first_datapoint = datapoint_group[0]
    const row = {
      campaign: moment(first_datapoint.campaign.start_date).format('MMM YYYY'),
      campaign_id: first_datapoint.campaign.id,
      location: first_datapoint.location.name,
      location_id: first_datapoint.location.id
    }
    datapoint_group.forEach(datapoint => row[datapoint.indicator.id] = datapoint)
    return row
  }) : []

  return rows
}

const _getColumnData = (grouped_datapoints, updateDatapoint, removeDatapoint) => {
  const first_row = _.toArray(grouped_datapoints)[0]
  const columns = first_row && first_row.length > 0 ? first_row.map(first_row_datapoint => {
    const column = {
      field: first_row_datapoint.indicator.id + '.value',
      headerName: first_row_datapoint.indicator.name,
      enableCellChangeFlash: true,
      cellStyle: {textAlign: 'center'}
    }
    column.cellRenderer = reactCellRendererFactory(cell => {
      const datapoint = cell.params.data[first_row_datapoint.indicator.id]
      const cellParams = Object.assign({}, cell.params, {datapoint, updateDatapoint, removeDatapoint})
      if (datapoint.indicator.data_format === 'bool') {
        return <BoolCell cellParams={cellParams}/>
      } else if (datapoint.indicator.data_format === 'pct') {
        return <PercentCell cellParams={cellParams}/>
      } else {
        return <IntegerCell cellParams={cellParams}/>
      }
    })
    return column
  }) : []
  columns.unshift({
    colWidth: 100,
    headerName: '',
    field: 'location',
    // pinned: 'left' // This causes a bug in ag-grid where the table keeps expanding.
  })
  return columns
}

export default DataEntryTable
