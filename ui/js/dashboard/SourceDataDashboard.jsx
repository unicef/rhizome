'use strict';

var _     = require('lodash');
var React = require('react');
var api = require('../data/api.js')
var moment = require('moment');
var page = require('page');

var AppActions          = require('actions/AppActions');
var Overview   = require('dashboard/nco/Overview.jsx');
var Breakdown  = require('dashboard/nco/Breakdown.jsx');
var CampaignTitleMenu   = require('component/CampaignTitleMenu.jsx');
var NavigationStore     = require('stores/NavigationStore');

var ResultsTable = require('doc-review/DocResults.js');
var MappingTable = require('doc-review/DocMapping.js');
var DocOverview = require('doc-review/DocOverview.js');
var TitleMenu  = require('component/TitleMenu.jsx');
var MenuItem            = require('component/MenuItem.jsx');


var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	Paginator, SearchBar,
	FilterPanel, FilterDateRange
	} = require('react-datascope');

var SourceDataDashboard = React.createClass({
  propTypes : {
    dashboard : React.PropTypes.object.isRequired,
    data      : React.PropTypes.object.isRequired,
    region    : React.PropTypes.object.isRequired,

    loading   : React.PropTypes.bool
  },

	getInitialState : function () {
    return {
      regions      : [],
      campaigns    : [],
      region       : null,
      campaign     : null,
      dashboard    : null,
    };
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var loading = this.props.loading;
		var region = this.props.region


		var docItems = MenuItem.fromArray(
			_.map(NavigationStore.documents, d => {
				return {
					title : d.docfile,
					value : d.id
				};
			}),
			this._setDocId);

		var doc_tools = MenuItem.fromArray(
			_.map(['overview','mapping','validate','results','dashboard'], d => {
				return {
					title : d,
					value : d
				};
			}),
			this._setDocTool);

		try {
			var doc_id = this.state.doc_id
		}
		catch(err) {
			var doc_id = -1
		}

		var docName = doc_id
		var doc_tool = 'validate'


		var parseSchema = require('../ufadmin/utils/parseSchema');
	  var some_schema = {"fields": [{"name": "id", "title": "id"},{"name": "campaign", "title": "campaign"}]}
		var schema = parseSchema(some_schema)

		// navigation to set doc-id and doc-processor //
		var review_nav =
		<div className="admin-container">
			<h1 className="admin-header"></h1>
			<div className="row">
				document_id: <TitleMenu text={docName}>
					{docItems}
				</TitleMenu>
			</div>
			<div className="row">
			<TitleMenu text={doc_tool}>
				{doc_tools}
			</TitleMenu>
			</div>
		</div>;

		// data table //
		var review_table = <MappingTable
					region={region}
					loading={loading}
					doc_id={doc_id}
					>
				</MappingTable>

		var review_breakdown = <DocOverview
			doc_id={doc_id}
			loading={loading}
			>
		</DocOverview>

		return (<div className="row">
					<div className="medium-9 columns">
						{review_table}
					</div>
					<div className="medium-3 columns">
						{review_nav}
						{review_breakdown}
					</div>
		</div>);;
  },

	_setDocId : function (doc_id) {
		console.log('loading_new_document_id')
		this._navigate({ doc_id : doc_id });
		this._navigate({ doc_id : doc_id });
		this.state.doc_id = doc_id
		return {}
	},


	_navigate : function (params) {
		var slug     = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title));
		var region   = _.get(params, 'region', this.props.region.name);
		var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'));
		var doc_id = _.get(params, 'doc_id', this.state.doc_id);

		if (_.isNumber(region)) {
			region = _.find(this.state.regions, r => r.id === region).name;
		}
		console.log('NAVIGATING')
    page('/datapoints/' + [slug, region, campaign].join('/') + '#' + doc_id);
	},

});

module.exports = SourceDataDashboard;
