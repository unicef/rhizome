var _ = require('lodash');
var React = require('react/addons');
var API = require('../data/api');
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

var parseSchema = require('../ufadmin/utils/parseSchema');

var ReviewPage = React.createClass({
	propTypes: {
		title: React.PropTypes.string.isRequired,
		getMetadata: React.PropTypes.func.isRequired,
		getData: React.PropTypes.func.isRequired,
    loading   : React.PropTypes.bool,
	},
	getInitialState: function() {
		return {
			data: null,
			schema: null,
			query: {},
			areFiltersVisible: false,
			loading   : false
		}
	},


	componentWillMount: function() {
		this.props.getMetadata().then(response => this.setState({
			metadata: response,
			schema: parseSchema(response)
		}));
		this.props.getData().then(response => this.setState({data: response.objects}));
		},

	onToggleFilterContainer() {
		this.setState(prevState => ({areFiltersVisible: !prevState.areFiltersVisible}));
	},

	render() {
		// render loading indicator until data has loaded

		// var isLoaded = _.isArray(this.state.data) && this.state.metadata && this.state.schema;
		// if(!isLoaded) return this.renderLoading();

		if (this.state.loading) return this.renderLoading();
		var isLoaded = _.isArray(this.state.data) && this.state.metadata && this.state.schema;
		if(!isLoaded) return this.renderLoading();

		var {data, schema, metadata} = this.state;

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

		console.log('rendering the datascope data, schema and fields..')
		console.log(data)
		console.log(schema)
		console.log(fields)

		return <div>
			<LocalDatascope data={data} schema={schema} fields={fields} pageSize={25}>
				<Datascope>
					{this.props.children}
				</Datascope>
			</LocalDatascope>
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'> .... Review Page Loading .... </div>
	},
	renderFilters() {
		var filterExpander = this.state.areFiltersVisible ? '[-]' : '[+]';
		var { areFiltersVisible } = this.state;

		return <div className="ufadmin-filters-container">
			<div className="ufadmin-show-filters" onClick={this.onToggleFilterContainer}>

				{areFiltersVisible ?
					<span>
						<ClearQueryLink>
							Filter results {filterExpander}
						</ClearQueryLink>
						<span onClick={e => {e.stopPropagation()}}>
							<ClearQueryLink>
								<a className='admin-clear-filters'>Clear filters</a>
							</ClearQueryLink>
						</span>
					</span>
				:
					<span>Filter results {filterExpander}</span>
				}
			</div>


			{areFiltersVisible ?
				<div className="ufadmin-filters-content">
					{this.props.datascopeFilters}
				</div>
			: null}
		</div>
	}
});


module.exports = ReviewPage;
