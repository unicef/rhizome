var React = require('react/addons');
var _ = require('lodash');

var api = require('../data/api');

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
		campaign 	: React.PropTypes.object.isRequired,
		doc_id 	: React.PropTypes.number.isRequired,
		doc_tab 	: React.PropTypes.string.isRequired,

		loading : React.PropTypes.bool
	},

	getDefaultProps : function () {
		return {
			loading : false
		};
	},

	render() {

		var loading = this.props.loading
		var doc_id = this.props.doc_id
		var region = this.props.region
		var campaign = this.props.campaign

		if(loading && !(doc_id)) return this.renderLoading();

		var parseSchema = require('../ufadmin/utils/parseSchema');
		var some_schema = {"fields": [{"name": "id", "title": "id"},{"name": "campaign", "title": "campaign"}]}
		var schema = parseSchema(some_schema)


		return <ReviewPage
			title="ToMap"
			getMetadata={api.admin.docMapMeta}
			getData={api.admin.docMap}
			schema={schema}
			fields={fields}
			loading={loading}
			doc_id={doc_id}
			region={region}
			campaign={campaign}
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
