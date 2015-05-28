var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator,
	SearchBar
} = require('react-datascope');
var AdminPage = require('./AdminPage');

var RegionsAdmin = React.createClass({
	render() {
		return <AdminPage
			title="Regions"
			getMetadata={API.admin.regionsMetadata}
			getData={API.admin.regions}
			>
			<LocalDatascope pageSize={100}>
				<Datascope>
					<SearchBar placeholder="search regions"/>
					<Paginator />
					<SimpleDataTable>
						<SimpleDataTableColumn name="id" />
						<SimpleDataTableColumn name="region_code" />
						<SimpleDataTableColumn name="name" />
						<SimpleDataTableColumn name="slug" />
						<SimpleDataTableColumn name="is_high_risk" />
						<SimpleDataTableColumn name="latitude" />
						<SimpleDataTableColumn name="longitude" />
						<SimpleDataTableColumn name="created_at" />
					</SimpleDataTable>
				</Datascope>
			</LocalDatascope>
		</AdminPage>
	}
});

module.exports = RegionsAdmin;
