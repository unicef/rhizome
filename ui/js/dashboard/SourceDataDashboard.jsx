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

// var Router = require('react-router');
// var {Route, DefaultRoute, RouteHandler,NotFoundRoute, NotFound, Redirect, Link} = Router;

var SourceDataDashboard = React.createClass({
  propTypes : {
    dashboard : React.PropTypes.object.isRequired,
    data      : React.PropTypes.object.isRequired,
    region    : React.PropTypes.object.isRequired,
    doc_id    : React.PropTypes.number.isRequired,

    loading   : React.PropTypes.bool
  },

	componentWillUpdate : function (nextProps, nextState) {
    console.log('hi this is john logging')
		console.log(nextProps)
		console.log(nextState)
		if (!(nextState.campaign && nextState.region && nextState.dashboard)) {
      return;
    }

    var campaign = moment(nextState.campaign.start_date).format('MM/YYYY')
    var title = [
      nextState.dashboard.title,
      [nextState.region.name, campaign].join(' '),
      'RhizomeDB'
    ].join(' - ');

    if (document.title !== title) {
      document.title = title;
    }
  },
	// console.log(this.parent)
  _navigate : function (params) {
    var slug     = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title));
    var region   = _.get(params, 'region', this.props.region.name);
    var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'));

		var doc_id = params.doc_id
		console.log('this dot state')
		console.log(this.state)

    page('/datapoints/' + [slug, region, campaign].join('/') + '#' + doc_id);
  },

	getInitialState : function () {
    return {
      regions      : [],
      campaigns    : [],
      region       : null,
      campaign     : null,
      dashboard    : null,
			doc_id			 : null,
    };
  },


	_setDocId : function (doc_id) {
		console.log('loading_new_document_id')
		this._navigate({ doc_id : doc_id });
    // this.setState({ doc_id : doc_id })
		return {}
	},

	_setDocTask : function (doc_task) {
		this._navigate({ doc_slug : doc_task });
	},

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var loading = this.props.loading;

		console.log(this.props)

    const fields = {
    	map_link: {
    		title: 'Master Object Name',
    		key: 'id',
    		renderer: (id) => {
    				return MapButtonFunction(id)
    			}
    	},
    };

		try {
			var doc_id = this.props.doc_id
		}
		catch(err) {
			var doc_id = 5
		}

		const fieldNamesOnTable = ['id','slug'];

    var data_fn = function(){
				return api.admin.campaigns()
    };

		var meta_fn = function(){
				return api.admin.campaignsMetadata()
		};

		var docItems = MenuItem.fromArray(
			_.map(NavigationStore.documents, d => {
				return {
					title : d.docfile,
					value : d.id
				};
			}),
			this._setDocId);

		var docName = 'sample doc'

		var review_header =
		<div className="admin-container">
      <h1 className="admin-header"></h1>
			<TitleMenu text={docName}>
				{docItems}
			</TitleMenu>
			<ul className="admin-nav">
			<li><a href="#overview">Overview</a></li>
			<li><a href="#mapping">Mapping</a></li>
			<li><a href="#validate">Validate</a></li>
			<li><a href="#results">Results</a></li>
			</ul>
    </div>;

		var refreshMasterUrl = '/source_data/refresh_master/' + doc_id
		var refreshMasterButton = refreshMasterUrl ?
			<div className="ufadmin-create-button">
				<a className="button" href={refreshMasterUrl}>Refresh Master</a>
			</div> : null;

		return (<div>
    		{review_header}
				<h2> Document ID :  </h2>
				{refreshMasterButton}
		    <ReviewPage
  			title="ToMap"
  			getMetadata={meta_fn}
  			getData={data_fn}
  			fields={fields}
  			>
  				<Paginator />
  				<SimpleDataTable>
  					{fieldNamesOnTable.map(fieldName => {
  						return <SimpleDataTableColumn name={fieldName} />
  					})}
  				</SimpleDataTable>
  		</ReviewPage>
    </div>);;
  }
});





module.exports = SourceDataDashboard;
