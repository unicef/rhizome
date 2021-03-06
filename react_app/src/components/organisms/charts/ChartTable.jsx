import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import Placeholder from 'components/global/Placeholder'

const columnDefs = [
  {headerName: "ID", field: "id"},
  {headerName: "Title", field: "title"},
  {headerName: 'Countries', field: 'countries', hide: true},
  {headerName: 'EndDate', field: 'endDate', hide: true},
  {headerName: 'GroupBy', field: 'groupBy', hide: true},
  {headerName: 'Id', field: 'id', hide: true},
  {headerName: 'Indicators', field: 'indicators', hide: true},
  {headerName: 'Location_id', field: 'location_id', hide: true},
  {headerName: 'Location_ids', field: 'location_ids', hide: true},
  {headerName: 'Locations', field: 'locations', hide: true},
  {headerName: 'StartDate', field: 'startDate', hide: true},
  {headerName: 'TimeRange', field: 'timeRange', hide: true},
  {headerName: 'Title', field: 'title', hide: true},
  {headerName: 'Type', field: 'type', hide: true},
  {headerName: 'X', field: 'x', hide: true},
  {headerName: 'XFormat', field: 'xFormat', hide: true},
  {headerName: 'Y', field: 'y', hide: true},
  {headerName: 'YFormat', field: 'yFormat', hide: true},
  {headerName: 'Z', field: 'z', hide: true},
]

const ChartTable = ({ charts, getAllCharts }) => {
  return charts.raw ? (
    <ResourceTable
      rowData={charts.raw}
      onRefreshData={() => getAllCharts()}
      columnDefs={columnDefs}
      resourcePath='charts' />
  ) : <Placeholder />
}

export default ChartTable
