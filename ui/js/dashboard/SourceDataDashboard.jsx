'use strict';

var _     = require('lodash');
var React = require('react');
var api = require('../data/api.js')
var moment = require('moment');
var page = require('page');

var AppActions          = require('actions/AppActions');
var Overview   = require('dashboard/nco/Overview.jsx');
var Breakdown  = require('dashboard/nco/Breakdown.jsx');
var ReviewPage = require('../doc-review/ReviewPage');
var TitleMenu  = require('component/TitleMenu.jsx');
var CampaignTitleMenu   = require('component/CampaignTitleMenu.jsx');
var MenuItem            = require('component/MenuItem.jsx');
var NavigationStore     = require('stores/NavigationStore');

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
    doc_id    : React.PropTypes.number.isRequired,

    loading   : React.PropTypes.bool
  },

	componentWillMount : function () {
		page('/datapoints/:dashboard/:region/:year/:month', this._show);
		page('/datapoints/:dashboard', this._showDefault);
		AppActions.init();
	},

	componentWillUpdate : function (nextProps, nextState) {

    var campaign = moment(nextProps.campaign.start_date).format('MM/YYYY')
    var title = [
      nextProps.dashboard.title,
      [nextProps.region.name, campaign].join(' '),
      'RhizomeDB'
    ].join(' - ') + nextState.doc_id;
    if (document.title !== title) {
      document.title = title;
    }
  },
	// console.log(this.parent)
  _navigate : function (params) {
    var slug     = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title));
    var region   = _.get(params, 'region', this.props.region.name);
    var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'));
		var doc_id = _.get(params, 'doc_id', this.state.doc_id);
		var doc_tool = _.get(params, 'doc_tool', this.state.doc_tool);

    page('/datapoints/' + [slug, region, campaign].join('/') + '#' + doc_id + '/' + doc_tool);
  },
	_showDefault : function (ctx) {
	},

	_show : function (ctx) {
	},


	getInitialState : function () {
    return {
      regions      : [],
      campaigns    : [],
      region       : null,
      campaign     : null,
      dashboard    : null,
			doc_id			 : 66,
			doc_tool 		 : 'overview'
    };
  },


	_setDocId : function (doc_id) {
		console.log('loading_new_document_id')
		this._navigate({ doc_id : doc_id });
		this.state.doc_id = doc_id
		this.props.data = this.data_fn()
		return {}

	},

	_setDocTool : function (doc_tool) {
		this._navigate({ doc_tool : doc_tool });
		this.state.doc_tool = doc_tool
		return {loading : true}
	},

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

	data_fn : function(){
		return api.admin.docValidate({document:this.state.doc_id})
	},

	meta_fn : function(){
			return api.admin.docValidateMeta()
	},

  render : function () {
    var loading = this.props.loading;
    const fields = {
    	map_link: {
    		title: 'Master Object Name',
    		key: 'id',
    		renderer: (id) => {
    				return MapButtonFunction(id)
    			}
    	},
    };

		var doc_id = this.state.doc_id

		const fieldNamesOnTable = ['id','document_id'];
		var doc_tool = this.state.doc_tool;

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

		var docName = doc_id

		var review_header =
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

		var refreshMasterUrl = '/source_data/refresh_master/' + doc_id
		var refreshMasterButton = refreshMasterUrl ?
			<div className="ufadmin-create-button">
				<a className="button" href={refreshMasterUrl}>Refresh Master</a>
			</div> : null;

		return (<div className="row">
					<div className="medium-9 columns">
			    <ReviewPage
	  			title="ToMap"
	  			getMetadata={this.meta_fn}
	  			getData={this.data_fn}
	  			fields={fields}
	  			>
	  				<Paginator />
						<SimpleDataTable>
	  					{fieldNamesOnTable.map(fieldName => {
	  						return <SimpleDataTableColumn name={fieldName} />
	  					})}
	  				</SimpleDataTable>
	  		</ReviewPage>
    	</div>
			<div className="medium-3 columns">
			{review_header}
			<h2> Document ID : {doc_id} </h2>
			{refreshMasterButton}
			</div>
		</div>);;
  }
});





module.exports = SourceDataDashboard;
