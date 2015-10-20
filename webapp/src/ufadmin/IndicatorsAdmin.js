var React = require('react');
var _ = require('lodash');

var api = require('../data/api');

var {
  Datascope, LocalDatascope,
  SimpleDataTable, SimpleDataTableColumn,
  Paginator, SearchBar
  } = require('react-datascope');
var AdminPage = require('./AdminPage');

const fields = {
  edit_link: {
    title: 'Edit',
    key: 'id',
    renderer: (id) => {
      return <a href={`/ufadmin/manage/indicator/${id}`}>Edit Indicator</a>;
    }
  },
  id: {title: "ID", name: "id"},
  slug: {title: "Slug", name: 'slug'},
  short_name: {title: 'Short Name', name: 'short_name'},
  name: {title: 'Name', name: 'name'},
  description: {title: 'Description', name: 'description'}
};

const fieldNamesOnTable = ['id', 'slug', 'short_name', 'name', 'description', 'edit_link'];

// console.log(this.props);

var IndicatorsAdmin = React.createClass({
  render() {
    var datascopeFilters =
      <div>
        <SearchBar
          fieldNames={fieldNamesOnTable}
          placeholder="Search indicators ..."
          />
      </div>;

    return <AdminPage
      title="Indicators"
      getData={api.indicators}
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
});

module.exports = IndicatorsAdmin;
