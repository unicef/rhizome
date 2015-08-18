'use strict';

var _     = require('lodash');
var React = require('react');
var api = require('../data/api.js')

var Overview   = require('dashboard/nco/Overview.jsx');
var Breakdown  = require('dashboard/nco/Breakdown.jsx');
var ReviewPage = require('../doc-review/ReviewPage');
// var TitleMenu  = require('component/TitleMenu.jsx');
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

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var data    = this.props.data; // i should populate this with the data call from doc review
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

    var doc_id = 72;
    const fieldNamesOnTable = ['id','content_type','source_object_code','master_object_id'];

    var data_fn = function(){
      return api.admin.docMap({document:doc_id},null,{'cache-control':'no-cache'})
    };

		// console.log(this.props)

		var campaign = this.props.region
		var campaigns = this.props.indicators

		var review_header =
		<div className="admin-container">
      <h1 className="admin-header"></h1>
      <ul className="admin-nav">
      <li><a className="" href="/datapoints/source-data/Alkaleri/2015/03/">Home</a></li>
      <li><a className="" href="/datapoints/source-data/Alkaleri/2015/03/">Mapping</a></li>
      <li><a className="" href="/datapoints/source-data/Alkaleri/2015/03/">Mapping</a></li>
      <li><a className="" href="/datapoints/source-data/Alkaleri/2015/03/">Validate</a></li>
      <li><a className="" href="/datapoints/source-data/Alkaleri/2015/03/">View Results</a></li>
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
  			getMetadata={api.admin.docMapMeta}
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
