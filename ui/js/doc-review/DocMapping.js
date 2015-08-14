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


const fieldNamesOnTable = ['id','master_object_id','master_dp_count','map_id'];

// const fieldNamesOnTable = ['id'];


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
			return API.doc_review_meta({document_id:doc_id},null,{'cache-control':'no-cache'})
		};


		return <ReviewPage
			title="ToMap"
			getMetadata={API.doc_review_meta}
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
