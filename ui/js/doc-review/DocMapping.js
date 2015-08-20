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

const fieldNamesOnTable = ['id','content_type','source_object_code','master_object_id'];

var DocMapping = React.createClass({
	propTypes : {
		region 	: React.PropTypes.object.isRequired,
		doc_id 	: React.PropTypes.number.isRequired,
		loading : React.PropTypes.bool
	},

	getDefaultProps : function () {
		return {
			loading : false
		};
	},

	dataFn : function(){
		console.log('calling the database with props.docId')
		console.log(this.props.doc_id)
		return API.admin.docMap({},null,{'cache-control':'no-cache'})
	},

	render() {

		var loading = this.props.loading
		var doc_id = this.props.doc_id
		var region = this.props.region

		if(loading && !(doc_id)) return this.renderLoading();

		var meta_fn = function(){
			return API.admin.docMapMeta()
		};

		return <ReviewPage
			title="ToMap"
			getMetadata={meta_fn}
			getData={this.dataFn}
			fields={fields}
			loading={loading}
			doc_id={doc_id}
			>
				<Paginator />
				<SimpleDataTable>
					{fieldNamesOnTable.map(fieldName => {
						return <SimpleDataTableColumn name={fieldName} />
					})}
				</SimpleDataTable>
		</ReviewPage>
	},
	renderLoading() {
		return <div className='admin-loading'>.......Loading Map Data.........</div>
	},
});

module.exports = DocMapping;
