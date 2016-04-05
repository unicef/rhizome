import React from 'react'

import AdminPage from 'components/organisms/ufadmin/AdminPage'

import TableToRefactor from 'components/organisms/datascope/TableToRefactor'
import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
import Paginator from 'components/organisms/datascope/Paginator'
import SearchBar from 'components/organisms/datascope/SearchBar'

import api from 'data/api'

// display rules for datascope fields
const checkmarkRenderer = (val) => val ? '✓' : ''
const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => <a href={`/users/update/${id}`}>Edit User</a>
  },
  is_active: { title: 'active?', renderer: checkmarkRenderer },
  is_staff: { title: 'staff?', renderer: checkmarkRenderer },
  is_superuser: { title: 'superuser?', renderer: checkmarkRenderer },
  date_joined: { format: 'MMM D YYYY' },
  id: { title: 'ID', name: 'id' },
  username: { title: 'User Name', name: 'username' },
  first_name: { title: 'First Name', name: 'first_name' },
  last_name: { title: 'Last Name', name: 'last_name' },
  email: { title: 'Email', name: 'email' }
}

const schema = {
  last_login: { type: 'string', format: 'date-time' }
}

const fieldNamesOnTable = ['id', 'username', 'first_name', 'last_name', 'email', 'edit_link']

const UsersAdmin = React.createClass({
  getInitialState () {
    return { areFiltersVisible: true }
  },

  render () {
    var datascopeFilters = (
      <div>
        <SearchBar
          fieldNames={['id', 'username', 'first_name', 'last_name', 'email', 'edit_link']}
          placeholder='Search users ...'
        />
      </div>
    )

    return (
      <AdminPage
        title='Users'
        getData={api.users}
        fields={fields}
        schema={schema}
        datascopeFilters={datascopeFilters} >
        <Paginator />
        <TableToRefactor>
          { fieldNamesOnTable.map(fieldName => {
            return <SimpleDataTableColumn name={fieldName}/>
          })}
        </TableToRefactor>
      </AdminPage>
    )
  }
})

export default UsersAdmin
