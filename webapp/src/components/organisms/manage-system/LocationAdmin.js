import React from 'react'

import TableToRefactor from 'components/organisms/datascope/TableToRefactor'
import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
import Paginator from 'components/organisms/datascope/Paginator'
import SearchBar from 'components/organisms/datascope/SearchBar'

import api from 'data/api'

import AdminPage from 'components/organisms/manage-system/AdminPage'

const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => {
      return <a href={`/locations/update/${id}`}>Edit location</a>
    }
  },
  id: { title: 'ID', name: 'id' },
  name: { title: 'Name', name: 'name' },
  location_code: { title: 'Location code', name: 'location_code' },
  created_at: { title: 'Created At', name: 'created_at', format: 'MMM D YYYY, h:mm a' }
}

const schema = {
  created_at: { type: 'string', format: 'date-time' }
}

const fieldNamesOnTable = ['id', 'name', 'location_code', 'created_at', 'edit_link']

var LocationAdmin = React.createClass({
  render () {
    var datascopeFilters =
      <div>
        <SearchBar
          fieldNames={['id', 'name', 'location_code']}
          placeholder='Search locations ...'
          />
      </div>

    return <AdminPage
      title='Locations'
      getData={api.locations}
      datascopeFilters={datascopeFilters}
      fields={fields}
      schema={schema}
      >
      <Paginator />
      <TableToRefactor>
        {fieldNamesOnTable.map(fieldName => {
          return <SimpleDataTableColumn name={fieldName}/>
        })}
      </TableToRefactor>
    </AdminPage>
  }
})

export default LocationAdmin
