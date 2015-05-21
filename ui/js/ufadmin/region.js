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


var RegionAdmin = React.createClass({
	getInitialState: function() {
		return {
			query: {}
		};
	},
	componentDidMount: function() {
		API.admin.regionsMetadata().done(response => {
			var schema = parseSchema(response);
			console.log('schema', schema);
			this.setState({schema: schema});
		});
		API.admin.regions().done(response => {
			this.setState({regions: response.objects.slice(0,30)});


		});
	},
	onChangeQuery: function(query) {
		this.setState({query});
	},

	render: function() {
		var isLoaded = _.isArray(this.state.regions) && this.state.schema && this.state.schema.items;
		if(!isLoaded) return this.renderLoading();

		return (
			<div>
				<h1>Regions Admin Page (first 30)</h1>
				<LocalDatascope
					data={this.state.regions}
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

module.exports = RegionAdmin;
