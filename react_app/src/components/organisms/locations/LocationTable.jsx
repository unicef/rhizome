import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import Placeholder from 'components/global/Placeholder'

const columnDefs = [
  {headerName: "ID", field: "id"},
  {headerName: "Name", field: "name"}
]

const LocationTable = ({ locations, getAllLocations }) => {
  return locations.raw ? (
  <ResourceTable
    rowData={locations.raw}
    onRefreshData={() => getAllLocations()}
    columnDefs={columnDefs}
    resourcePath='locations' />
  ) : <Placeholder />
}

export default LocationTable
