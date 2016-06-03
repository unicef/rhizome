import React from 'react'
import api from 'utilities/api'

import AdminPage from 'components/organisms/manage-system/AdminPage'

import TableToRefactor from 'components/organisms/datascope/TableToRefactor'
import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
import Paginator from 'components/organisms/datascope/Paginator'
import SearchBar from 'components/organisms/datascope/SearchBar'

const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => {
      return <a href={`/campaign/${id}`}>Edit Campaign</a>
    }
  },
  id: { title: 'ID', name: 'id' },
  name: { title: 'Display Name', name: 'name' },
  start_date: { title: 'Start Date', name: 'start_date' },
  end_date: { title: 'End Date', name: 'end_date' },
  created_at: { title: 'Created At', name: 'created_at', format: 'MMM D YYYY, h:mm a' }
}

const schema = {
  created_at: { type: 'string', format: 'date-time' }
}

const fieldNamesOnTable = ['id', 'name', 'start_date', 'end_date', 'created_at', 'edit_link']

var CampaignsAdmin = React.createClass({
  render () {
    var datascopeFilters = (
      <div>
        <SearchBar
          placeholder='Search campaigns ...'
          fieldNames={['id', 'slug', 'edit_link']}
          />
      </div>
    )

    return (
      <AdminPage
        title='Campaigns'
        getData={api.campaign}
        schema={schema}
        datascopeFilters={datascopeFilters}
        fields={fields} >
        <Paginator />
        <TableToRefactor>
          {fieldNamesOnTable.map(fieldName => {
            return <SimpleDataTableColumn name={fieldName}/>
          })}
        </TableToRefactor>
      </AdminPage>
    )
  }
})

export default CampaignsAdmin
