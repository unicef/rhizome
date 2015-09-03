var React = require('react');
var _ = require('lodash');

var api = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator, SearchBar
	} = require('react-datascope');
var AdminPage = require('./AdminPage');

const fields = {
	edit_link: {
		title: 'Edit',
		key: 'id',
		renderer: (id) => {
			return <a href={`/datapoints/indicators/update/${id}`}>Edit Indicator</a>;
		}
	}
};

const fieldNamesOnTable = ['id', 'slug', 'short_name', 'name', 'description', 'edit_link'];

// console.log(this.props);

var IndicatorsAdmin = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar placeholder="search indicators"/>
			</div>;

		return <AdminPage
			title="Indicators"
			getData={api.indicators}
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

module.exports = IndicatorsAdmin;
