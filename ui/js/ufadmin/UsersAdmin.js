var React = require('react/addons');
var _ = require('lodash');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn
} = require('react-datascope');
var AdminPage = require('./AdminPage');

var API = require('../data/api');

var UsersAdmin = React.createClass({
	render() {
		return <AdminPage
			title="Users"
			getMetadata={API.admin.usersMetadata}
			getData={API.admin.users}
			>
			<LocalDatascope>
				<Datascope>
					<SimpleDataTable>
						<SimpleDataTableColumn name="id" />
						<SimpleDataTableColumn name="username" />
						<SimpleDataTableColumn name="first_name" />
						<SimpleDataTableColumn name="last_name" />
						<SimpleDataTableColumn name="email" />
						<SimpleDataTableColumn name="is_active" />
						<SimpleDataTableColumn name="is_staff" />
						<SimpleDataTableColumn name="is_superuser" />
						<SimpleDataTableColumn name="date_joined" />
						<SimpleDataTableColumn name="last_login" />
					</SimpleDataTable>
				</Datascope>
			</LocalDatascope>
		</AdminPage>
	}
});

module.exports = UsersAdmin;
