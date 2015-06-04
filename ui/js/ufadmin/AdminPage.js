var _ = require('lodash');
var React = require('react/addons');
const {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator,
	SearchBar,
	FilterPanel, FilterDateRange, FilterInputRadio
	} = require('react-datascope');

var parseSchema = require('./utils/parseSchema');

var AdminPage = React.createClass({
	propTypes: {
		title: React.PropTypes.string.isRequired,
		getMetadata: React.PropTypes.func.isRequired,
		getData: React.PropTypes.func.isRequired
	},
	getInitialState: function() {
		return {
			data: null,
			schema: null,
			query: {},
			areFiltersVisible: false
		}
	},

	componentWillMount: function() {
		this.props.getMetadata().done(response => this.setState({
			metadata: response,
			schema: parseSchema(response)
		}));
		this.props.getData().done(response => this.setState({data: response.objects}));
	},

	onToggleFilterContainer() {
		this.setState((prevState) => ({areFiltersVisible: !prevState.areFiltersVisible}));
	},

	render() {
		// render loading indicator until data has loaded
		var isLoaded = _.isArray(this.state.data) && this.state.metadata && this.state.schema;
		if(!isLoaded) return this.renderLoading();

		var {data, schema, metadata} = this.state;

		// make the "Create X" button if we have a creation URL
		var createUrl = _.get(metadata, 'objects.url_patterns.create', null);
		if(createUrl) createUrl = '/' + createUrl;
		// strip the "s" from the end of plural title
		var titleSingular = _.endsWith(this.props.title, 's') ? _.initial(this.props.title).join('') : this.props.title;
		var createButton = createUrl ?
			<div className="ufadmin-create-button">
				<a className="button" href={createUrl}>Create {titleSingular}</a>
			</div> : null;

		return <div>
			<h2 className="ufadmin-page-heading">{this.props.title} Admin Page</h2>

			{createButton}

			<LocalDatascope data={data} schema={schema} fields={this.props.fields} pageSize={100}>
				<Datascope>

					{this.props.datascopeFilters ? this.renderFilters(): null}

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

		return <div className="ufadmin-filters-container">
			<div className="ufadmin-show-filters" onClick={this.onToggleFilterContainer}>
				Filter results {filterExpander}
			</div>

			{this.state.areFiltersVisible ?
				<div className="ufadmin-filters-content">
					{this.props.datascopeFilters}
				</div>
			: null}
		</div>
	}
});


module.exports = AdminPage;
