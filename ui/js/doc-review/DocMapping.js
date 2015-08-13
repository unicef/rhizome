var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator, SearchBar,
	FilterPanel, FilterDateRange
	} = require('react-datascope');

var ReviewPage = require('./ReviewPage');

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
};

const fieldNamesOnTable = ['slug', 'start_date', 'end_date', 'edit_link'];

var DocMapping = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar placeholder="search campaigns"/>
				<FilterPanel>
					<FilterDateRange name="start_date" time={false} />
					<FilterDateRange name="end_date" time={false} />
					</FilterPanel>
			</div>;

		return <ReviewPage
			title="ToMap"
			getMetadata={API.admin.docsMetadata}
			getData={API.admin.docs}
			datascopeFilters={datascopeFilters}
			fields={fields}
			>
				<Paginator />
				<SimpleDataTable>
					{fieldNamesOnTable.map(fieldName => {
						return <SimpleDataTableColumn name={fieldName} />
					})}
				</SimpleDataTable>
		</ReviewPage>
	}
});

module.exports = DocMapping;
