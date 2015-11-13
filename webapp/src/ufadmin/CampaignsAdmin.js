import React from 'react'
import api from '../data/api'

var {
  SimpleDataTable, SimpleDataTableColumn,
  Paginator, SearchBar
} = require('react-datascope')
import AdminPage from './AdminPage'

const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => {
      return <a href={`/datapoints/campaigns/update/${id}`}>Edit Campaign</a>
    }
  },
  id: { title: 'ID', name: 'id' },
  slug: { title: 'Display Name', name: 'slug' },
  start_date: { title: 'Start Date', name: 'start_date' },
  end_date: { title: 'End Date', name: 'end_date' },
  created_at: { title: 'Created At', name: 'created_at', format: 'MMM D YYYY, h:mm a' }
}

const schema = {
  created_at: { type: 'string', format: 'date-time' }
}

const fieldNamesOnTable = ['id', 'slug', 'start_date', 'end_date', 'created_at', 'edit_link']

var CampaignsAdmin = React.createClass({
  render () {
    var datascopeFilters =
      <div>
        <SearchBar
          placeholder='Search campaigns ...'
          fieldNames={['id', 'slug', 'edit_link']}
          />
      </div>

    return <AdminPage
      title='Campaigns'
      getData={api.campaign}
      schema={schema}
      datascopeFilters={datascopeFilters}
      fields={fields}
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

module.exports = CampaignsAdmin
