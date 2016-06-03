import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'

const columnDefs = [
  {headerName: "ID", field: "id", suppressMenu: true},
  {headerName: "Short Name", field: "short_name", editable: true},
  {headerName: "Name", field: "name"},
  {headerName: "Description", field: "description"},
  {headerName: 'Is_reported', field: 'is_reported', hide: true},
  {headerName: 'Created_at', field: 'created_at', hide: true},
  {headerName: 'Data_format', field: 'data_format', hide: true},
  {headerName: 'Bound_json', field: 'bound_json', hide: true},
  {headerName: 'Office_id', field: 'office_id', hide: true},
  {headerName: 'Tag_json', field: 'tag_json', hide: true},
  {headerName: 'High_bound', field: 'high_bound', hide: true},
  {headerName: 'Low_bound', field: 'low_bound', hide: true},
  {headerName: 'Source_name', field: 'source_name', hide: true}
]

const IndicatorTable = ({ indicators, fetchIndicators }) => {
  return (
    <ResourceTable
      rowData={_.toArray(indicators)}
      onRefreshData={fetchIndicators}
      columnDefs={columnDefs}
      resourcePath='indicators'
    />
  )
}

export default IndicatorTable