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
    var data    = this.props.data;
    var loading = this.props.loading;

    console.log(data)
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
    const fieldNamesOnTable = ['id','content_type','source_object_code','master_object_id'];

    var data_fn = function(){
      return api.admin.docMap({document:doc_id},null,{'cache-control':'no-cache'})
    };

    return (<ReviewPage
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

    );
  }
});

module.exports = SourceDataDashboard;
