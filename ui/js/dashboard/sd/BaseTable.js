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
				return;
			}
		},

	componentWillReceiveProps: function(nextProps) {
		console.log('NEW PROPSS!!!!')
		this.props.getMetadata().then(response => this.setState({
			metadata: response,
			schema: parseSchema(response)
		}));
		this.props.getData({master_object_id:nextProps.region.id},null,{'cache-control':'no-cache'}).then(response => this.setState({data: response.objects}));
		this.forceUpdate()
		},
	render() {

		var isLoaded = _.isArray(this.state.data) && this.state.metadata && this.state.schema && (!this.state.loading);
		if(!isLoaded) return this.renderLoading();

		var {data, schema, metadata} = this.state;

		var fields = this.props.fields

		console.log('returning render of review page')
		console.log(data.length)
		console.log('tat was the len of the data..')

		return <div>
			<LocalDatascope data={data} schema={schema} fields={fields} pageSize={25}>
				<Datascope>
					{this.props.children}
				</Datascope>
			</LocalDatascope>
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'> Review Page Loading...</div>
	},
});


module.exports = ReviewPage;
