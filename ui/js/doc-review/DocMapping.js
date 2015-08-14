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
	// edit_link: {
	// 	title: 'Edit',
	// 	key: 'id',
	// 	renderer: (id) => {
	// 		return <a href={`/datapoints/campaigns/update/${id}`}>Edit Campaign</a>;
	// 	}
	// },
};


// const fieldNamesOnTable = ['id','source_string','master_display_name','edit_link'];
const fieldNamesOnTable = ['source_string'];


var DocMapping = React.createClass({
	render() {

		var doc_id = this.props.params.docId

		var datascopeFilters =
			<div>
				<SearchBar placeholder="search campaigns"/>
				<FilterPanel>
					<FilterDateRange name="start_date" time={false} />
					<FilterDateRange name="end_date" time={false} />
					</FilterPanel>
			</div>;

		var data_fn = function(){
			return API.docs({document_id:doc_id},null,{'cache-control':'no-cache'})
		};

		return <ReviewPage
			title="ToMap"
			getMetadata={API.admin.docsMetadata}
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
