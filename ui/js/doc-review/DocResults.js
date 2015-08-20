var React = require('react/addons');
var _ = require('lodash');

var API = require('../data/api');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator, SearchBar,
	FilterPanel, FilterDateRange
	} = require('react-datascope');


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

const fieldNamesOnTable = ['id','map_link'];

var DocResults = React.createClass({
	render() {

		// var doc_id = this.props.params.docId

		return <LocalDatascope
				data={this.props.data}
				schema={this.props.schema}
				fields={this.props.fields}
				pageSize={25}>
				<Datascope>
				<Paginator />
				<SimpleDataTable>
					{fieldNamesOnTable.map(fieldName => {
						return <SimpleDataTableColumn name={fieldName} />
					})}
				</SimpleDataTable>
				</Datascope>
			</LocalDatascope>
	}
});

module.exports = DocResults;
