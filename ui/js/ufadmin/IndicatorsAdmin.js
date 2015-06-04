var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

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

var IndicatorsAdmin = React.createClass({
	render() {
		var datascopeFilters =
			<div>
				<SearchBar placeholder="search indicators"/>
			</div>;

		return <AdminPage
			title="Indicators"
			getMetadata={API.admin.indicatorsMetadata}
			getData={API.admin.indicators}
			datascopeFilters={datascopeFilters}
			fields={fields}
			>
				<Paginator />
				<SimpleDataTable>
					<SimpleDataTableColumn name="id" />
					<SimpleDataTableColumn name="slug" />
					<SimpleDataTableColumn name="short_name" />
					<SimpleDataTableColumn name="name" />
					<SimpleDataTableColumn name="description" />
					<SimpleDataTableColumn name="edit_link" />
				</SimpleDataTable>
		</AdminPage>
	}
});

module.exports = IndicatorsAdmin;

