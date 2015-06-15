'use strict';

var _ = require('lodash');
var React = require('react');

var DonutChart = require('component/DonutChart.jsx');
var Chart = require('component/Chart.jsx')

var Monitoring = React.createClass({
  propTypes : {
    data    : React.PropTypes.object.isRequired,
    loading : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var loading = this.props.loading;
    var data    = this.props.data;

    var options = {
      innerRadius : 0.6,
      domain      : _.constant([0, 1])
    };

    return (
      <div className='row'>

        <div className='medium-6 columns'>
          <div className='row'>
            <div className='small-12 columns'>
              <h4 style={{ textAlign: 'center' }}>Missed Children</h4>
            </div>

            <div className='medium-6 columns'>
              <DonutChart data={data.inside} loading={loading} options={options} />
            </div>

            <div className='medium-6 columns'>
              <DonutChart data={data.outside} loading={loading} options={options} />
            </div>
          </div>
        </div>

        <div className='medium-6 columns'>
          <div className='row'>
            <div className='small-12 columns'>
              <h4 style={{ textAlign : 'center' }}>Caregiver Awareness</h4>
            </div>

            <div className='medium-6 push-3 end columns'>
              <DonutChart data={data.caregiverAwareness} loading={loading} options={options} />
            </div>

          </div>
        </div>
      </div>
    );
  }

});

module.exports = Monitoring;
