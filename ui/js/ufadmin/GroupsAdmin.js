var React = require('react/addons');
var _ = require('lodash');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator,
	SearchBar,
	FilterPanel, FilterDateRange, FilterInputRadio
} = require('react-datascope');

var API = require('../data/api');

var AdminPage = require('./AdminPage');

// display rules for datascope fields
const checkmarkRenderer = (val) => val ? "✓" : "";
const fields = {
	edit_link: {
		title: 'Edit',
		key: 'id',
		renderer: (id) => {
			return <a href={`/datapoints/groups/update/${id}`}>Edit Group</a>;
		}
	}
};

const fieldNamesOnTable = ['name', 'edit_link'];

var GroupsAdmin = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar
					fieldNames={['name']}
					placeholder="search groups"
					/>
			</div>;

		return <AdminPage
			title="Groups"
			getMetadata={API.admin.groupsMetadata}
			getData={API.admin.groups}
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
});

module.exports = GroupsAdmin;
