var React = require('react')

var api = require('../data/api')

var {
  Datascope, LocalDatascope,
  SimpleDataTable, SimpleDataTableColumn,
  Paginator, SearchBar
  } = require('react-datascope')
var AdminPage = require('./AdminPage')

const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => {
      return <a href={`/ufadmin/manage/indicator_tag/${id}`}>Edit Tags</a>
    }
  },
  id: { title: 'ID', name: 'id' },
  tag_name: { title: 'Tag Name', name: 'tag_name' },
  parent_tag_id: { title: 'Parent Tag Id', name: 'parent_tag_id' },
  parent_tag__tag_name: { title: 'Parent Tag Name', name: 'parent_tag__tag_name' }
}

const fieldNamesOnTable = ['id', 'tag_name', 'parent_tag_id', 'parent_tag__tag_name', 'edit_link']

// console.log(this.props)

var TagsAdmin = React.createClass({
  render () {
    var datascopeFilters =
      <div>
        <SearchBar
          placeholder='Search tags ...'
          fieldNames={fieldNamesOnTable}
          />
      </div>

    return <AdminPage
      title='Tags'
      getData={api.get_indicator_tag}
      datascopeFilters={datascopeFilters}
      fields={fields}
      >
        <Paginator />
        <SimpleDataTable>
          {fieldNamesOnTable.map(fieldName => {
            return <SimpleDataTableColumn name={fieldName} />
          })}
        </SimpleDataTable>
    </AdminPage>
  }
})

module.exports = TagsAdmin
