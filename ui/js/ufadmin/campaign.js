var React = require('react/addons');
var _ = require('lodash');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	SearchBar,
	FilterPanel, FilterInputCheckbox
	} = require('react-datascope');

var API = require('../data/api');
var mockData = require('./utils/mockdata');
var parseSchema = require('./utils/parseSchema');


var CampaignAdmin = React.createClass({
	getInitialState: function() {
		return {
			query: {}
		};
	},
	componentDidMount: function() {
		API.admin.campaignsMetadata().done(response => {
			var schema = parseSchema(response);
			console.log('schema', schema);
			this.setState({schema: schema});
		});
		API.admin.campaigns().done(response => {
			this.setState({campaigns: response.objects});
		});
	},
	onChangeQuery: function(query) {
		this.setState({query});
	},

	render: function() {
		var isLoaded = _.isArray(this.state.campaigns) && this.state.schema && this.state.schema.items;
		if(!isLoaded) return this.renderLoading();

		//var propSchemas = this.state.schema.items.properties,
		//	searchableFieldNames = propSchemas ?
		//		_(propSchemas).keys().filter(k => propSchemas[k].searchable).value() : [];
		console.log('state', this.state);

		return (
			<div>
				<h1>Campaigns Admin Page</h1>
				<LocalDatascope
					data={this.state.campaigns}
					schema={this.state.schema}
					onChangeQuery={this.onChangeQuery}
					>
					<Datascope>
						<SimpleDataTable>
						</SimpleDataTable>
					</Datascope>
				</LocalDatascope>
			</div>
		)
	},
	renderLoading() {
		return <div className='admin-loading'>Loading...</div>
	}
});

module.exports = CampaignAdmin;
