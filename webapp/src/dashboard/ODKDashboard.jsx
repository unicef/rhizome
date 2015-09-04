'use strict';

var _     = require('lodash');
var React = require('react');
var ODKOverview = require('dashboard/odk/ODKOverview.jsx');
var ODKMap = require('dashboard/odk/ODKmap.jsx');
var ODKBreakdown = require('dashboard/odk/ODKBreakdown.jsx');

var NCODashboard = React.createClass({
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


    return (
      <div id='nco-dashboard'>
        <section>
          <div className='row'>
            <div className='small-6 columns'>
              <h3>{this.props.region.name} - Overview</h3>
              <ODKOverview
               loading={loading}
               data={data}
              />
            </div>
            <div className='small-6 columns'>
              <h3>{this.props.region.name} - Non Compliance </h3>
              <ODKMap
               loading={loading}
               data={data}
              />
            </div>
          </div>
        </section>
        <section>
          <ODKBreakdown data={data} loading={loading} />
        </section>

      </div>
    );
  }
});

module.exports = NCODashboard;
