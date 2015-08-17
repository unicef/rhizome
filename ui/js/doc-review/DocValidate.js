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

var MapButtonFunction = function(data){
	return <a href={`/datapoints/campaigns/update/${data}`}> THIS IS JOHN </a>;
}

const fields = {
	map_link: {
		title: 'Master Object Name',
		key: 'id',
		renderer: (id) => {
				return MapButtonFunction(id)
			}
	},
};


const fieldNamesOnTable = ['id','region_id','campaign_id','indicator_id','value'];

var DocValidate = React.createClass({
	render() {

		var doc_id = this.props.params.docId

		var datascopeFilters =
			<div>
				<SearchBar placeholder="..search.."/>
				<FilterPanel>
					// <FilterDateRange name="start_date" time={false} />
					// <FilterDateRange name="end_date" time={false} />
					</FilterPanel>
			</div>;

		var data_fn = function(){
			return API.admin.docValidate({document:doc_id},null,{'cache-control':'no-cache'})
		};

		return <ReviewPage
			title="Validation Page"
			getMetadata={API.admin.DataPointMetaData}
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

module.exports = DocValidate;
