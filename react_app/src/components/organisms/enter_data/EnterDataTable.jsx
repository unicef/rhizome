import _ from 'lodash'
import React from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import moment from 'moment'
import format from 'utilities/format'
import {reactCellRendererFactory} from 'ag-grid-react'
import IntegerCell from 'components/table/IntegerCell'
import BoolCell from 'components/table/BoolCell'
import PercentCell from 'components/table/PercentCell'

const EnterDataTable = (props) => {
  const datapoints = props.datapoints.flattened
  const grouped_datapoints = _.groupBy(datapoints, 'location.id')
  const rows = _getRowData(grouped_datapoints)
  const columns = _getColumnData(grouped_datapoints, props.updateDatapoint)
  return (
    <ResourceTable
      rowData={rows}
      columnDefs={columns}
      resourcePath='datapoints'
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

const _getColumnData = (grouped_datapoints, updateDatapoint) => {
  const first_row = _.toArray(grouped_datapoints)[0]
  const columns = first_row.length > 0 ? first_row.map(datapoint => {
    const column = {
      field: datapoint.indicator.id + '.value',
      headerName: datapoint.indicator.name
    }
    column.cellRenderer = reactCellRendererFactory(params => {
      const cellParams = Object.assign({}, params, {datapoint, updateDatapoint})
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
  columns.unshift({headerName: '', field: 'location'})
  return columns
}

export default EnterDataTable
