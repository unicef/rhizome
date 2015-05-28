var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator
	} = require('react-datascope');
var AdminPage = require('./AdminPage');

var CampaignsAdmin = React.createClass({
	render() {
		return <AdminPage
			title="Campaigns"
			getMetadata={API.admin.campaignsMetadata}
			getData={API.admin.campaigns}
			>
			<LocalDatascope>
				<Datascope>
					<Paginator />
					<SimpleDataTable>
						<SimpleDataTableColumn name="id" />
						<SimpleDataTableColumn name="slug" />
						<SimpleDataTableColumn name="start_date" />
						<SimpleDataTableColumn name="end_date" />
						<SimpleDataTableColumn name="created_at" />
					</SimpleDataTable>
				</Datascope>
			</LocalDatascope>
		</AdminPage>
	}
});

module.exports = CampaignsAdmin;


