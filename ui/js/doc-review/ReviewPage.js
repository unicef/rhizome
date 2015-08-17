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
		getData: React.PropTypes.func.isRequired
	},
	getInitialState: function() {
		return {
			data: null,
			schema: null,
			indicators: null,
			campaigns: null,
			regions: null,
			query: {},
			areFiltersVisible: false
		}
	},

	componentDidMount: function() {

	API.indicatorsTree().then(function(result) {
			var indicator_api_data = result.objects;
			this.setState({indicators:indicator_api_data});
		}.bind(this));

	API.admin.regions().then(function(result) {
			var region_api_data = result.objects;
			this.setState({regions:region_api_data});
		}.bind(this));

	API.admin.campaigns().then(function(result) {
			var campaign_api_data = result.objects;
			this.setState({campaigns:campaign_api_data});
		}.bind(this));
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

	updateIndicatorSelection: function() {
				console.log('updating indicator selection')
	},

	render() {
		// render loading indicator until data has loaded
		var isLoaded = _.isArray(this.state.data) && this.state.metadata && this.state.schema && this.state.campaigns && this.state.regions && this.state.indicators;
		if(!isLoaded) return this.renderLoading();

		var {data, schema, metadata, campaigns, regions, indicators} = this.state;

		console.log(campaigns)

		var dropDownFilters = (<div>
			<IndicatorDropdownMenu
			text='Filter Indicators'
			indicators={indicators}
			sendValue={this.updateIndicatorSelection}>
			</IndicatorDropdownMenu>

			<CampaignDropdownMenu
			title='filter campaigns'
			campaigns={campaigns}
			campaign={campaigns[0]}
			sendValue={this.updateIndicatorSelection}>
			</CampaignDropdownMenu>

			<RegionTitleMenu
			regions={regions}
			selected={regions[0]}
			sendValue={this.updateIndicatorSelection}>
			</RegionTitleMenu>
		</div>);

		return <div>

			<LocalDatascope data={data} schema={schema} fields={this.props.fields} pageSize={100}>
				<Datascope>

					<div className='row'>
					{dropDownFilters}
					</div>

					{this.props.children}

				</Datascope>
			</LocalDatascope>
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'>Loading...</div>
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
