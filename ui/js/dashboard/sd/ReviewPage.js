var _ = require('lodash');
var React = require('react/addons');
var API = require('data/api');
var RegionTitleMenu     = require('component/RegionTitleMenu.jsx');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');
var BaseTable =  require('dashboard/sd/BaseTable.js');

const {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	ClearQueryLink,
	Paginator,
	SearchBar,
	FilterPanel, FilterDateRange, FilterInputRadio
	} = require('react-datascope');

var parseSchema = require('ufadmin/utils/parseSchema');

var ReviewPage = React.createClass({
	propTypes: {
		title: React.PropTypes.string.isRequired,
		getMetadata: React.PropTypes.func.isRequired,
		getData: React.PropTypes.func.isRequired,
    loading   : React.PropTypes.bool.isRequired,
		fields 		: React.PropTypes.object.isRequired,
		region 		: React.PropTypes.object.isRequired,
	},
	getInitialState: function() {
		return {
			data: null,
			schema: null,
			query: {},
			loading   : false,
		}
	},

	componentWillMount: function() {
		this.props.getMetadata().then(response => this.setState({
			metadata: response,
			schema: parseSchema(response)
		}));
		this.props.getData({master_object_id:this.props.region.id},null,{'cache-control':'no-cache'}).then(response => this.setState({data: response.objects}));
		},

	componentWillUpdate : function (nextProps, nextState) {
		// update this.state.data if there is a metadata change //
			if (nextProps.region != this.props.region) {
				console.log('updating!')
				return;
			console.log('not updating')
			}
		},

	componentWillReceiveProps: function(nextProps) {
		this.props.getData({master_object_id:nextProps.region.id},null,{'cache-control':'no-cache'}).then(response => this.setState({data: response.objects}));
		this.forceUpdate()
		},
	render() {

		var isLoaded = _.isArray(this.state.data) && this.state.metadata && this.state.schema && (!this.state.loading);
		if(!isLoaded) return this.renderLoading();

		var {data, schema, metadata} = this.state;
		var fields = this.props.fields

		var region_name = _.kebabCase(this.props.region.name);

		console.log('this is data len')
		console.log(data.length)

		return <div>
		<div>
			<h1> make this table below dynamic </h1>
			<BaseTable key={region_name} data={data} schema={schema} pageSize={25} isLoaded={isLoaded} datascope_data={this.props.children} >
			</BaseTable>
		</div>
		 <div>	<h1>OLD TABLE  </h1>
        <LocalDatascope key={region_name} data={data} schema={schema} pageSize={25}>
	         <Datascope>
	           {this.props.children}
	         </Datascope>
         </LocalDatascope>
    </div>
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'> Review Page Loading...</div>
	},
});


module.exports = ReviewPage;
