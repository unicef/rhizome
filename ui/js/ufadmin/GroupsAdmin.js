var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator
} = require('react-datascope');
var AdminPage = require('./AdminPage');

var GroupsAdmin = React.createClass({
	render() {
		return <AdminPage
			title="Groups"
			getMetadata={API.admin.groupsMetadata}
			getData={API.admin.groups}
			>
			<LocalDatascope>
				<Datascope>
					<Paginator />
					<SimpleDataTable>
					</SimpleDataTable>
				</Datascope>
			</LocalDatascope>
		</AdminPage>
	}
});

module.exports = GroupsAdmin;
