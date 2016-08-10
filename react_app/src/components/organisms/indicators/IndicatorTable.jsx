import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import Placeholder from 'components/global/Placeholder'

const columnDefs = [
  {headerName: "ID", field: "id", suppressMenu: true},
  {headerName: "Short Name", field: "short_name", editable: true},
  {headerName: "Name", field: "name"},
  {headerName: "Description", field: "description"},
  {headerName: 'Is_reported', field: 'is_reported', hide: true},
  {headerName: 'Created_at', field: 'created_at', hide: true},
  {headerName: 'Data_format', field: 'data_format', hide: true},
  {headerName: 'Bound_json', field: 'bound_json', hide: true},
  {headerName: 'Tag_json', field: 'tag_json', hide: true},
  {headerName: 'High_bound', field: 'high_bound', hide: true},
  {headerName: 'Low_bound', field: 'low_bound', hide: true},
  {headerName: 'Source_name', field: 'source_name', hide: true}
]

const IndicatorTable = ({ indicators, getAllIndicators }) => {
  return indicators.raw ? (
    <ResourceTable
      rowData={indicators.raw}
      onRefreshData={() => getAllIndicators()}
      columnDefs={columnDefs}
      resourcePath='indicators'
    />
  ) : <Placeholder />
}

export default IndicatorTable
