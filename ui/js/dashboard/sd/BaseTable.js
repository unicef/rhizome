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
		data 			: React.PropTypes.object.isRequired,
		schema 		: React.PropTypes.object.isRequired,
		fields 		: React.PropTypes.object.isRequired,
		loading   : React.PropTypes.bool.isRequired,

	},
	getInitialState: function() {
		return {
			data: null,
			schema: null,
			fields: [],
			loading   : false,
		}
	},

	render() {

		var loading = this.props.loading
		if(loading) return this.renderLoading();

		var {data, schema, fields} = this.props;

		return <div>
			<LocalDatascope data={data} schema={schema} fields={fields} pageSize={25}>
				<Datascope>
					{this.props.children}
				</Datascope>
			</LocalDatascope>
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'> BaseTable Loading...</div>
	},
});


module.exports = BaseTable;
