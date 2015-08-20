var _ = require('lodash');
var React = require('react/addons');
var API = require('data/api');
var RegionTitleMenu     = require('component/RegionTitleMenu.jsx');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');

const {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	ClearQueryLink,
	Paginator,
	SearchBar,
	FilterPanel, FilterDateRange, FilterInputRadio
	} = require('react-datascope');


var BaseTable = React.createClass({
	propTypes: {
		data 			: React.PropTypes.array.isRequired,
		schema 		: React.PropTypes.object.isRequired,
		loading   : React.PropTypes.bool.isRequired,
		datascope_data : React.PropTypes.object.isRequired,

	},
	getInitialState: function() {
		return {
			data: null,
			schema: null,
			fields: [],
			isLoaded   : false,
		}
	},

	render() {

		var data = this.props.data;
		var schema = this.props.schema
		var datascope_data = this.props.datascope_data
		
		console.log('render??? loading??')

		var isLoaded = _.isArray(data) && schema;
		if(!isLoaded) return this.renderLoading();

		console.log('renddderrr')
		console.log(data)
		console.log(schema)
		return <div>
			SOMETHING
			<LocalDatascope data={data} schema={schema} pageSize={25}>
				<Datascope>
					{datascope_data}
				</Datascope>
			</LocalDatascope>
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'> BaseTable Loading...</div>
	},
});


module.exports = BaseTable;
