import React from 'react'

import api from 'data/api'

import TableToRefactor from 'components/organisms/datascope/TableToRefactor'
import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
import Paginator from 'components/organisms/datascope/Paginator'
import SearchBar from 'components/organisms/datascope/SearchBar'

import AdminPage from 'components/organisms/ufadmin/AdminPage'

const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => {
      return <a href={`/manage_system/manage/indicator/${id}`}>Edit Indicator</a>
    }
  },
  id: { title: 'ID', name: 'id' },
  short_name: { title: 'Short Name', name: 'short_name' },
  name: { title: 'Name', name: 'name' },
  description: { title: 'Description', name: 'description' }
}

const fieldNamesOnTable = ['id', 'short_name', 'name', 'description', 'edit_link']

var IndicatorsAdmin = React.createClass({
  render () {
    var datascopeFilters = (
      <div>
        <SearchBar
          fieldNames={fieldNamesOnTable}
          placeholder='Search indicators ...'
        />
      </div>
    )

    return (
      <AdminPage
        title='Indicators'
        getData={api.indicators}
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

export default IndicatorsAdmin
