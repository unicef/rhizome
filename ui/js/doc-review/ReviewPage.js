var _ = require('lodash');
var React = require('react/addons');
var API = require('../data/api');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');


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
			query: {},
			areFiltersVisible: false
		}
	},

	componentWillMount: function() {
		this.props.getMetadata().then(response => this.setState({
			metadata: response,
			schema: parseSchema(response)
		}));
		this.props.getData().then(response => this.setState({data: response.objects}));
		API.indicatorsTree().then(response => this.setState({indicators: response.objects}));
	},

	onToggleFilterContainer() {
		this.setState(prevState => ({areFiltersVisible: !prevState.areFiltersVisible}));
	},


	render() {
		// render loading indicator until data has loaded
		var isLoaded = _.isArray(this.state.data) && this.state.metadata && this.state.schema && this.state.indicators;
		if(!isLoaded) return this.renderLoading();

		var {data, schema, metadata, indicators} = this.state;

		console.log('===')
		console.log(indicators)
		console.log('===')

		// strip the "s" from the end of plural title
		var titleSingular = _.endsWith(this.props.title, 's') ? _.initial(this.props.title).join('') : this.props.title;

		var updateIndicatorSelection = function() {
					console.log('updating indicator selection')
		};

		// var x = [];

		var indicatorsSection = (<div>
								<IndicatorDropdownMenu
									text='Filter Indicators'
									indicators={indicators}
									sendValue={updateIndicatorSelection}>
								</IndicatorDropdownMenu>
								{indicators}
							</div>);

		return <div>

			<LocalDatascope data={data} schema={schema} fields={this.props.fields} pageSize={100}>
				<Datascope>

					{indicatorsSection}

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
