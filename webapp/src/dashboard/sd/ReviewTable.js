var _											= require('lodash');
var React 								= require('react');
var RegionTitleMenu     	= require('component/RegionTitleMenu.jsx');
var DashboardStore    		= require('stores/DashboardStore');
var GroupFormStore 				= require('stores/GroupFormStore');
var ChartBuilderStore 		= require('stores/ChartBuilderStore');

var MapForm 							= require('dashboard/sd/MapForm.js');
var api 									= require('data/api.js');

const {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	ClearQueryLink,
	Paginator,
	SearchBar,
	FilterPanel, FilterDateRange, FilterInputRadio
	} = require('react-datascope');

var parseSchema = require('ufadmin/utils/parseSchema');

var ReviewTable = React.createClass({
	propTypes: {
		title: React.PropTypes.string.isRequired,
		getMetadata: React.PropTypes.func.isRequired,
		getData: React.PropTypes.func.isRequired,
    loading   : React.PropTypes.bool.isRequired,
		region 		: React.PropTypes.object.isRequired,
		campaign 	: React.PropTypes.object.isRequired,
		doc_tab 	: React.PropTypes.string.isRequired,
	},

	getInitialState: function() {
		return {
			data: null,
			schema: null,
			query: {},
			loading   : false,
		}
	},

	getDefaultProps : function () {
    return {
      loading : false
    };
  },

	validateForm : function(id){
			// onclick post to api..
			return <input type="checkbox" checked  />;
	},

	_callApi : function(){
		this.props.getMetadata()
		.then(response => this.setState({
				schema: parseSchema(response)
		}));

		this.props.getData({
				document_id:this.props.doc_id,
				region_id:this.props.region.id,
				campaign_id:this.props.campaign.id
			},null,{'cache-control':'no-cache'})
			.then(response => this.setState({
						data: response.objects
			}));
			this.forceUpdate();
	},

	componentWillMount: function() {
		api.indicatorsTree().then(indicators => this.setState({
				indicators: indicators
		}));

		this._callApi()
		},

	componentWillReceiveProps: function(nextProps) {
		this._callApi()
	},

	componentWillUpdate : function (nextProps, nextState) {
			// FIXME -> needs cleanup
			if (nextProps.region != this.props.region) {
				console.log('updagin with  new regions')
				return;
			}
			if (nextProps.getMetadata != this.props.getMetadata) {
				console.log('bring up a new table')
				return;
			}
			if (nextProps.doc_id != this.props.doc_id) {
				console.log('new doc id')
				return;
			}
		},


	render() {

		console.log(this.state.indicators)
		
		const fields = {
			is_valid: {
				title: 'Edit',
				key: 'id',
				renderer: (id) => {
						if (this.props.doc_tab == 'validate') {
							return this.validateForm(id)
						}
						else if (this.props.doc_tab == 'mapping') {
							return <MapForm
											indicators={this.state.indicators}
											campaigns={DashboardStore.campaigns}
											regions={DashboardStore.regions}
							 				source_object_map_id={id}
											key={id}
											/>
					}
				}
			},
		};

		var isLoaded = _.isArray(this.state.data) && this.state.schema && (!this.state.loading);
		if(!isLoaded) return this.renderLoading();

		var {data, schema} = this.state;

		return <div>
        <LocalDatascope
				 		data={data}
						schema={schema}
						fields={fields}
						pageSize={25}>
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


module.exports = ReviewTable;
