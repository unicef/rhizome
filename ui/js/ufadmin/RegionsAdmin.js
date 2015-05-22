var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn
} = require('react-datascope');
var AdminPage = require('./AdminPage');

var RegionsAdmin = React.createClass({
	render() {
		return <AdminPage
			title="Regions"
			getMetadata={API.admin.regionsMetadata}
			getData={API.admin.regions}
			>
			<LocalDatascope>
				<Datascope>
					<SimpleDataTable>
					</SimpleDataTable>
				</Datascope>
			</LocalDatascope>
		</AdminPage>
	}
});

module.exports = RegionsAdmin;
