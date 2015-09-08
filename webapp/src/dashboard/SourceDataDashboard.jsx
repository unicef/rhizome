'use strict';

var _     	= require('lodash');
var React		= require('react');
var api 		= require('data/api.js')
var moment 	= require('moment');
var page 		= require('page');

var NavigationStore    	= require('stores/NavigationStore');
var ReviewTable = require('dashboard/sd/ReviewTable.js');
var DocOverview = require('dashboard/sd/DocOverview.js');

var TitleMenu  	= require('component/TitleMenu.jsx');
var RegionTitleMenu  	= require('component/RegionTitleMenu.jsx');
var MenuItem    = require('component/MenuItem.jsx');
var ReactCSSTransitionGroup = require('react/lib/ReactCSSTransitionGroup');


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
		regions   : React.PropTypes.object.isRequired,
		doc_id    : React.PropTypes.number.isRequired,
		doc_tab    : React.PropTypes.string.isRequired,

    loading   : React.PropTypes.bool
  },


  render : function () {
    var loading = this.props.loading;
		var campaign = this.props.campaign;
		var region = this.props.region;
		var loading = this.props.loading;
		var doc_id = this.props.doc_id;
		var doc_tab = this.props.doc_tab

		if (! doc_tab) {
			var doc_tab = 'doc_index'
		}

		var docItems = MenuItem.fromArray(
			_.map(NavigationStore.documents, d => {
				return {
					title : d.docfile,
					value : d.id
				};
			}),
			this._setDocId);

		var doc_tabs = MenuItem.fromArray(
			_.map(['viewraw','mapping','validate','results','doc_index'], d => {
				return {
					title : d,
					value : d
				};
			}),
			this._setDocTab);

		// navigation to set doc-id and doc-processor //
		var review_nav =
		<div className="admin-container">
			<h1 className="admin-header"></h1>
			<div className="row">
				document_id: <TitleMenu text={doc_id}>
					{docItems}
				</TitleMenu>
			</div>
			<div className="row">
			<TitleMenu text={doc_tab}>
				{doc_tabs}
			</TitleMenu>
			</div>
		</div>;

		const table_definition = {
			'viewraw':{
				'meta_fn' : api.submissionMeta,
				'data_fn' : api.submission,
				'fields' : ['id','username_code','region_code','campaign_code','region_display','edit_link'],
				'search_fields' :['id','username_code','region_code','campaign_code','region_display'],
			},
			'doc_index':{
				'data_fn' : api.source_doc,
				'fields' : ['id','docfile','edit_link'],
				'search_fields' :['id','docfile'],
			},
			'mapping':{
					'data_fn' : api.docMap,
					'fields' : ['id','content_type','source_object_code','master_object_id','master_object_name','edit_link'],
					'search_fields' :['id','content_type','source_object_code','master_object_id','master_object_name'],
				},
			'validate':{
				'data_fn' : api.docDatapoint,
				'fields' :['id','document_id','region_id','indicator_id','campaign_id','value','edit_link'],
				'search_fields' :['region_id','indicator_id','campaign_id'],
			},
			'results':{
				'data_fn' : api.docResults,
				'fields' : ['id','region_id','indicator_id','campaign_id','value'],
				'search_fields' :['region_id','indicator_id','campaign_id'],
			},
		};



	var search_fields = table_definition[doc_tab]['search_fields']
	var datascopeFilters =
		<div>
			<SearchBar
				fieldNames={search_fields}
				placeholder="search ..."
				/>
		</div>;

	var table_key = _.kebabCase(this.props.region.name) + this.props.campaign.slug + doc_id + doc_tab;
		// data table //
	var review_table = <ReviewTable
					title='sample title'
					getData={table_definition[doc_tab]['data_fn']}
					fields={table_definition[doc_tab]['fields']}
					region={region}
					key={table_key}
					loading={loading}
					doc_id={doc_id}
					doc_tab={doc_tab}
					campaign={campaign}
					datascopeFilters={datascopeFilters}
					>
					<Paginator />
					<SimpleDataTable>
						{table_definition[doc_tab]['fields'].map(fieldName => {
							return <SimpleDataTableColumn name={fieldName} />
						})}
					</SimpleDataTable>
			</ReviewTable>

		var review_breakdown = <DocOverview
			key={table_key + 'breakdown'}
			loading={loading}
			doc_id={doc_id}
			>
			</DocOverview>;

		return (
					<div className="row">
					<div id="popUp"></div>
					<div className="medium-9 columns">
					<h2 style={{ textAlign: 'left' }} className="ufadmin-page-heading">{doc_tab}</h2>
					{review_table}
					</div>
					<div className="medium-3 columns">
						{review_nav}
						{review_breakdown}
					</div>
		</div>);
	},

_setDocId : function (doc_id) {
	this._navigate({ doc_id : doc_id });
	this.forceUpdate();
},

_setDocTab : function (doc_tab) {
	this._navigate({ doc_tab : doc_tab });
	this.forceUpdate();
	},

_navigate : function (params) {
	var slug     = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title));
	var region   = _.get(params, 'region', this.props.region.name);
	var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'));
	var doc_tab = _.get(params, 'doc_tab', this.props.doc_tab);
	var doc_id = _.get(params, 'doc_id', this.props.doc_id);

	if (_.isNumber(region)) {
		region = _.find(this.state.regions, r => r.id === region).name;
	}

  page('/datapoints/' + [slug, region, campaign].join('/') + '/' + doc_tab + '/' + doc_id  );
},


});

module.exports = SourceDataDashboard;
