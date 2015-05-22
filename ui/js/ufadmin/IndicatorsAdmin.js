var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn
	} = require('react-datascope');
var AdminPage = require('./AdminPage');

var IndicatorsAdmin = React.createClass({
	render() {
		return <AdminPage
			title="Indicators"
			getMetadata={API.admin.indicatorsMetadata}
			getData={API.admin.indicators}
			>
			<LocalDatascope>
				<Datascope>
					<SimpleDataTable>
						<SimpleDataTableColumn name="id" />
						<SimpleDataTableColumn name="slug" />
						<SimpleDataTableColumn name="short_name" />
						<SimpleDataTableColumn name="name" />
						<SimpleDataTableColumn name="description" />
					</SimpleDataTable>
				</Datascope>
			</LocalDatascope>
		</AdminPage>
	}
});

module.exports = IndicatorsAdmin;
