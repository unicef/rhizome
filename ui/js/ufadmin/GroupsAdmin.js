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

var GroupsAdmin = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar placeholder="search groups"/>
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
					<SimpleDataTableColumn name="id" />
					<SimpleDataTableColumn name="name" />
					<SimpleDataTableColumn name="edit_link" />
				</SimpleDataTable>
		</AdminPage>
	}
});

module.exports = GroupsAdmin;
