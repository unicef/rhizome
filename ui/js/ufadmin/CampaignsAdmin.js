var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator, SearchBar,
	FilterPanel, FilterDateRange
	} = require('react-datascope');
var AdminPage = require('./AdminPage');

const fields = {
	edit_link: {
		title: 'Edit',
		key: 'id',
		renderer: (id) => {
			return <a href={`/datapoints/campaigns/update/${id}`}>Edit Campaign</a>;
		}
	},
	start_date: { format: 'MMM D YYYY' },
	end_date: { format: 'MMM D YYYY' },
	created_at: { format: 'MMM D YYYY, h:mm a' }
};

var CampaignsAdmin = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar placeholder="search campaigns"/>
				<FilterPanel>
					<FilterDateRange name="start_date" />
					<FilterDateRange name="end_date" />
					<FilterDateRange name="created_at" />
				</FilterPanel>
			</div>;

		return <AdminPage
			title="Campaigns"
			getMetadata={API.admin.campaignsMetadata}
			getData={API.admin.campaigns}
			datascopeFilters={datascopeFilters}
			fields={fields}
			>
				<Paginator />
				<SimpleDataTable>
					<SimpleDataTableColumn name="id" />
					<SimpleDataTableColumn name="slug" />
					<SimpleDataTableColumn name="start_date" />
					<SimpleDataTableColumn name="end_date" />
					<SimpleDataTableColumn name="created_at" />
					<SimpleDataTableColumn name="edit_link" />
				</SimpleDataTable>
		</AdminPage>
	}
});

module.exports = CampaignsAdmin;


