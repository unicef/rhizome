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
	propTypes : {
		data    : React.PropTypes.object.isRequired,
		region 	: React.PropTypes.object.isRequired,
		loading : React.PropTypes.bool
	},

	getDefaultProps : function () {
		return {
			loading : false
		};
	},

	render() {
		var data    = this.props.data;
		var region    = this.props.region;
	  var loading = this.props.loading;

		console.log(region)

		// var doc_id = this.props.params.docId
		return <LocalDatascope
				data={data}
				schema={this.props.schema}
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
	},

	renderLoading() {
		return <div className='admin-loading'>......Admin Loading.......</div>
	},

});

module.exports = DocResults;
