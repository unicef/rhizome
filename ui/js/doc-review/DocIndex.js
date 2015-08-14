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
			return <a href={`/doc_review/overview/${id}`}>View Document</a>;
		}
	},
};

const fieldNamesOnTable = ['id', 'created_by_id','docfile'];

var DocMapping = React.createClass({
	render() {

		var datascopeFilters =
			<div>
				<SearchBar placeholder="search document"/>
			</div>;

		var data_fn = function(){
			return API.document({},null,{'cache-control':'no-cache'})
		};

		var meta_fn = function(){
			return API.document_meta()
		};


		return <ReviewPage
			title="New Document "
			getMetadata={meta_fn}
			getData={data_fn}
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
