var React = require('react')
var _ = require('lodash')

var api = require('../data/api')

var {
  Datascope, LocalDatascope,
  SimpleDataTable, SimpleDataTableColumn,
  Paginator, SearchBar,
  FilterPanel, FilterDateRange
  } = require('react-datascope')
var AdminPage = require('./AdminPage')

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
