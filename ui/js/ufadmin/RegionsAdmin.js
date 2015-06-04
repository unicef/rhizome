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

const checkmarkRenderer = (val) => val ? "✓" : "";
const fields = {
	edit_link: {
		title: 'Edit',
		key: 'id',
		renderer: (id) => {
			return <a href={`/datapoints/regions/update/${id}`}>Edit Region</a>;
		}
	},
	created_at: { format: 'MMM D YYYY, h:mm a' },
	is_high_risk: { renderer: checkmarkRenderer }
};

var RegionsAdmin = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar placeholder="search regions"/>
				<FilterPanel>
					<FilterInputRadio name="is_high_risk" />
					<FilterDateRange name="created_at" />
				</FilterPanel>
			</div>;

		return <AdminPage
			title="Regions"
			getMetadata={API.admin.regionsMetadata}
			getData={API.admin.regions}
			datascopeFilters={datascopeFilters}
			fields={fields}
			>
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
					<SimpleDataTableColumn name="edit_link" />
				</SimpleDataTable>
		</AdminPage>
	}
});


module.exports = RegionsAdmin;
