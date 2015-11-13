'use strict'

import React from 'react'
var {
  SimpleDataTable, SimpleDataTableColumn,
  Paginator,
  SearchBar
} = require('react-datascope')

import api from '../data/api'

import AdminPage from './AdminPage'

const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => {
      return <a href={`/datapoints/locations/update/${id}`}>Edit location</a>
    }
  },
  id: { title: 'ID', name: 'id' },
  name: { title: 'Name', name: 'name' },
  created_at: { title: 'Created At', name: 'created_at', format: 'MMM D YYYY, h:mm a' }
}

const schema = {
  created_at: { type: 'string', format: 'date-time' }
}

const fieldNamesOnTable = ['id', 'name', 'created_at', 'edit_link']

var RegionAdmin = React.createClass({
  render () {
    var datascopeFilters =
      <div>
        <SearchBar
          fieldNames={['name']}
          placeholder='Search locations ...'
          />
      </div>

    return <AdminPage
      title='locations'
      getData={api.locations}
      datascopeFilters={datascopeFilters}
      fields={fields}
      schema={schema}
      >
      <Paginator />
      <SimpleDataTable>
        {fieldNamesOnTable.map(fieldName => {
          return <SimpleDataTableColumn name={fieldName}/>
        })}
      </SimpleDataTable>
    </AdminPage>
  }
})

export default RegionAdmin
