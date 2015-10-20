var React = require('react');
var _ = require('lodash');
var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator,
	SearchBar,
	FilterPanel, FilterDateRange, FilterInputRadio
	} = require('react-datascope');

var api = require('../data/api');

var AdminPage = require('./AdminPage');

const fields = {
	edit_link: {
		title: 'Edit',
		key: 'id',
		renderer: (id) => {
			return <a href={`/datapoints/locations/update/${id}`}>Edit location</a>;
		}
	},
	created_at: { format: 'MMM D YYYY, h:mm a' }
};

const fieldNamesOnTable = ['id', 'name', 'edit_link'];

var RegionAdmin = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar
					fieldNames={['name']}
					placeholder="Search locations ..."
					/>
			</div>;

		return <AdminPage
			title="locations"
			getData={api.locations}
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

module.exports = RegionAdmin;
