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

    var options = {
      values  : _.identity,
      x       : _.property('value'),
      xFormat : d3.format('%'),
      y       : _.property('indicator.short_name')
    };

    var headerStyle = {
      marginLeft : '80px'
    };

    return (
      <div>
        <div className='row'>
          <div className='medium-6 columns'>
            <Monitoring data={monitoring} loading={loading} />
          </div>

          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#influencers'>Influencers</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.influencers]} />
          </div>

          <div className='medium-3 columns'>
            <h4 style={headerStyle}><a href='#sources-of-information'>Information Sources</a></h4>
            <Chart
              type='BarChart'
              options={options}
              loading={loading}
              data={[data.informationSource]} />
          </div>
        </div>
      </div>
    );
  },
});

module.exports = Overview;
