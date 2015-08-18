'use strict';

var _     = require('lodash');
var React = require('react');
var api = require('../data/api.js')

var Overview   = require('dashboard/nco/Overview.jsx');
var Breakdown  = require('dashboard/nco/Breakdown.jsx');
var ReviewPage = require('../doc-review/ReviewPage');
var TitleMenu  = require('component/TitleMenu.jsx');
var CampaignTitleMenu   = require('component/CampaignTitleMenu.jsx');

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

    loading   : React.PropTypes.bool
  },

	logSomething : function () {
		console.log('LOAAAADING')
		return {}
	},

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var loading = this.props.loading;

		console.log('THIS DOT PROPS ')
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

    var doc_id = 72;
		const fieldNamesOnTable = ['id','slug'];

    var data_fn = function(){
				return api.admin.campaigns()
    };

		var meta_fn = function(){
				return api.admin.campaignsMetadata()
		};

		var docItems = [1,2,3,4]
		var docName = 'sample doc'

		var campaign = this.props.region
		var campaigns = this.props.indicators

		var review_header =
		<div className="admin-container">
      <h1 className="admin-header"></h1>
			<TitleMenu text={docName}>
				{docItems}
			</TitleMenu>
			<ul className="admin-nav">
			<li><a href="#Overview" onClick={this.logSomething}>Overview</a></li>
			<li><a href="#mapping" onClick={this.logSomething}>Mapping</a></li>
			<li><a href="#validate" onClick={this.logSomething}>Validate</a></li>
			<li><a href="#results" onClick={this.logSomething}>Results</a></li>
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
