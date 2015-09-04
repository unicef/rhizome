'use strict';

var _     = require('lodash');
var React = require('react');
var ODKOverview = require('dashboard/odk/ODKOverview.jsx');

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
            <div className='small-12 columns'>
              <h3>Overview for {this.props.region.name}</h3>
              <ODKOverview
               loading={loading}
               data={data}
              />
            </div>
          </div>
        </section>
      </div>
    );
  }
});

module.exports = NCODashboard;
