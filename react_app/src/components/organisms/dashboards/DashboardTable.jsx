import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import Placeholder from 'components/global/Placeholder'

const columnDefs = [
  {headerName: "ID", field: "id"},
  {headerName: "Title", field: "title"},
  {headerName: 'Description', field: 'description'}
]

const DashboardTable = ({ dashboards, getAllDashboards }) => {
  return dashboards.raw ? (
    <ResourceTable
      rowData={dashboards.raw}
      onRefreshData={() => getAllDashboards()}
      columnDefs={columnDefs}
      resourcePath='dashboards' />
  ) : <Placeholder />
}

export default DashboardTable
