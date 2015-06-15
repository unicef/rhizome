'use strict';

var _     = require('lodash');
var React = require('react');

var Chart      = require('component/Chart.jsx');
var Monitoring = require('dashboard/nco/Monitoring.jsx');

var Overview = React.createClass({
  propTypes : {
    data : React.PropTypes.object.isRequired,
    loading : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var loading    = this.props.loading;
    var data       = this.props.data;
    var monitoring = _.pick(data, 'inside', 'outside', 'caregiverAwareness',
      'insideMonitoring', 'outsideMonitoring');

    return (
      <div>
        <div className='mediium-6 columns'>
          <div className='row'>
            <div className='medium-6 columns'>
              <Monitoring data={monitoring} loading={loading} />
            </div>
          </div>
        </div>
      </div>
    );
  },
});

module.exports = Overview;
