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


	componentWillMount: function() {
		this.setState({data: this.props.data});

		// this.props.getData({master_object_id:this.props.region.id},null,{'cache-control':'no-cache'}).then(response => this.setState({data: response.objects}));
		},

	componentWillUpdate : function (nextProps, nextState) {
		if (nextProps.data != this.props.data) {

			var node = this.getDOMNode();
			React.unmountComponentAtNode(node);

			console.log('updating!')
			return;
		}
		},

	componentWillReceiveProps: function(nextProps) {
		this.setState({data: nextProps.data})
		this.forceUpdate()
		},

	render() {

		// var data = ;
		var schema = this.props.schema

		var isLoaded = _.isArray(this.state.data) && schema;
		if(!isLoaded) return this.renderLoading();

		console.log('the length of the data element is.. ' + (this.state.data).length)

		// var data = this.state.data

		var data = []

		return <div>
		<h2>Your Recent CSV Uploads</h2>
		<table>
			<tbody>{data}</tbody>
			<tfoot>
				<tr>
					<td className="more" colSpan="3">
						<a href="/source_data/document_index/">see all uploads</a>
					</td>
				</tr>
			</tfoot>
		</table>
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'> BaseTable Loading...</div>
	},
});


module.exports = BaseTable;
