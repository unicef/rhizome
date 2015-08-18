'use strict';

var _     = require('lodash');
var React = require('react');
var api = require('../data/api.js')

var Overview  = require('dashboard/nco/Overview.jsx');
var Breakdown = require('dashboard/nco/Breakdown.jsx');
var ReviewPage = require('../doc-review/ReviewPage');

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

    var review_header =  <div className="admin-container">
      <h1 className="admin-header">Document Review</h1>
      <ul className="admin-nav">
      <li><a className="" href="/doc_review/doc_index">Home</a></li>
      <li><a className="" href="/doc_review/overview/8">Mapping</a></li>
      <li><a className="" href="/doc_review/mapping/8">Mapping</a></li>
      <li><a className="" href="/doc_review/validate/8">Validate</a></li>
      <li><a className="" href="/doc_review/view_results/8">View Results</a></li>
      </ul>
    </div>;
    return (<div>
        {review_header}
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
    </div>);
  }
});

module.exports = SourceDataDashboard;
