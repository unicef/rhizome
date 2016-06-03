import _ from 'lodash'
import React, { PropTypes } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'

const columnDefs = [
  {headerName: "ID", field: "id"},
  {headerName: "Name", field: "name"}
]

const LocationTable = ({ locations, fetchLocations }) => {
  return (
  <ResourceTable
    rowData={_.toArray(locations)}
    onRefreshData={fetchLocations}
    columnDefs={columnDefs}
    resourcePath='locations' />
  )
}

LocationTable.propTypes = {
  locations: PropTypes.objectOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired
  }).isRequired)
}

export default LocationTable
