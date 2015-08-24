'use strict';

var _     	= require('lodash');
var React		= require('react');
var api 		= require('data/api.js')
var moment 	= require('moment');
var page 		= require('page');

var DashboardStore    	= require('stores/DashboardStore');
var NavigationStore    	= require('stores/NavigationStore');
var ReviewTable = require('dashboard/sd/ReviewTable.js');
var DocOverview = require('dashboard/sd/DocOverview.js');

var TitleMenu  	= require('component/TitleMenu.jsx');
var RegionTitleMenu  	= require('component/RegionTitleMenu.jsx');
var MenuItem    = require('component/MenuItem.jsx');
var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;
// var MapForm 		= require('dashboard/sd/MapForm.js')

var Modal = require('react-modal');

var appElement = document.getElementById('main');
Modal.setAppElement(appElement);
Modal.injectCSS();


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
		doc_id    : React.PropTypes.number,
		doc_tab    : React.PropTypes.string,

    loading   : React.PropTypes.bool
  },


	getInitialState : function () {
    return {
      regions      : [],
      campaigns    : [],
      region       : null,
      campaign     : null,
      dashboard    : null,
      doc_id    	 : 2,
			doc_tab    	 : 'mapping',
    	modalIsOpen	 : false,
		};
  },

	openModal: function() {
		this.setState({modalIsOpen: true});
	},

	closeModal: function() {
		this.setState({modalIsOpen: false});
	},

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

	postMetaMap : function(source_object_map_id) {
		console.log(source_object_map_id)
	},

	mapForm : function(source_object_map_id){ //, source_object_code

		var source_object_name = 'some-fake-metadata'
		var content_type = 'region'
		//
		var dropDown = <RegionTitleMenu
			                     regions={DashboardStore.regions}
													 selected={this.props.region}
			                     sendValue={this.postMetaMap} />
		//

		return <div><button className="tiny" onClick={this.openModal}> map! </button>
		        <Modal
		          isOpen={this.state.modalIsOpen}
		          onRequestClose={this.closeModal}
		        >
		          <h2>Mapping for {content_type} - {source_object_name} </h2>
		          <form>
							{dropDown}
		          </form>
		        </Modal></div>

	},

	validateForm : function(id){
			// onclick post to api..
			return <input type="checkbox" checked  />;
	},

  render : function () {
    var loading = this.props.loading;
		var campaign = this.props.campaign;
		var region = this.props.region;
		var loading = this.props.loading;
		var doc_id = this.state.doc_id;
		var doc_tab = this.props.doc_tab

		var docItems = MenuItem.fromArray(
			_.map(NavigationStore.documents, d => {
				return {
					title : d.docfile,
					value : d.id
				};
			}),
			this._setDocId);

		var doc_tabs = MenuItem.fromArray(
			_.map(['mapping','validate','results','doc_index'], d => {
				return {
					title : d,
					value : d
				};
			}),
			this._setDocTab);

		var doc_tab = this.state.doc_tab//this.state.doc_tab

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
			'doc_index':{
				'meta_fn' : api.document_meta,
				'data_fn' : api.document,
				'fields' : ['id','docfile'],
				'row_on_click' : null
			},
			'mapping':{
				  'meta_fn' : api.admin.docMapMeta,
					'data_fn' : api.admin.docMap,
					'fields' : ['id','content_type','source_object_code','master_object_name','is_valid'],
					'row_on_click' : null
				},
			'validate':{
				'meta_fn' : api.admin.docValidateMeta,
				'data_fn' : api.admin.docValidate,
				'fields' :['id','document_id','region_id','indicator_id','campaign_id','value','is_valid'],
				'row_on_click' : null
			},
			'results':{
				'meta_fn' : api.admin.DataPointMetaData,
				'data_fn' : api.admin.docResults,
				'fields' : ['id','region_id','indicator_id','campaign_id','value'],
				'row_on_click' : null
			},
		};

	const fields = {
		is_valid: {
			title: 'Edit',
			key: 'id',
			renderer: (id) => {
					if (this.state.doc_tab == 'validate') {
						return this.validateForm(id)
				}
					else if (this.state.doc_tab == 'mapping') {
						return this.mapForm(id)
				}
			}
		},
	};

	var table_key = _.kebabCase(this.props.region.name) + this.props.campaign.slug + doc_id + doc_tab;
		// data table //
	var review_table = <ReviewTable
					title='sample title'
					getMetadata={table_definition[doc_tab]['meta_fn']}
					getData={table_definition[doc_tab]['data_fn']}
					region={region}
					key={table_key}
					loading={loading}
					doc_id={doc_id}
					campaign={campaign}
					fields={fields}
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

		var table_title = doc_tab	 + ' for document_id: ' + doc_id;
		return (
					<div className="row">
					<div id="popUp"></div>
					<div className="medium-9 columns">
					<h2 style={{ textAlign: 'center' }} className="ufadmin-page-heading">{table_title}</h2>
					{review_table}
					</div>
					<div className="medium-3 columns">
						{review_nav}
						{review_breakdown}
					</div>
		</div>);
	}, // render

_setDocId : function (doc_id) {
	this._navigate({ doc_id : doc_id });
	this.state.doc_id = doc_id
	this.forceUpdate();
},

_setDocTab : function (doc_tab) {
	this._navigate({ doc_tab : doc_tab });
	this.state.doc_tab = doc_tab
	this.forceUpdate();
	},

_navigate : function (params) {
	var slug     = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title));
	var region   = _.get(params, 'region', this.props.region.name);
	var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'));
	var doc_id = _.get(params, 'doc_id', this.state.doc_id);

	if (_.isNumber(region)) {
		region = _.find(this.state.regions, r => r.id === region).name;
	}
  page('/datapoints/' + [slug, region, campaign].join('/') + '#' + doc_id);
},


});

module.exports = SourceDataDashboard;
