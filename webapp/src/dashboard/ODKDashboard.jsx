'use strict';

var _     = require('lodash');
var React = require('react');
var DonutChart = require('component/DonutChart.jsx');

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

    console.log('===OPEN DATA KIT===')
    console.log(data)

    var loading = this.props.loading;

    var options = {
      innerRadius : 0.6,
      domain      : _.constant([0, 1]),
      labelStyle  : {
        lineHeight : 1
      }
    };
    
    // var label = ..

    var caregiver_donut = <div className='row'>
      <div className='small-12 columns'>
        <h4 style={{ textAlign : 'center' }}>Caregiver Awareness</h4>
      </div>

      <div className='medium-6 push-3 end columns'>
        <DonutChart
          loading={loading}
          data={data.caregiverAwareness}
          options={options} />
      </div>

    </div>



    return (
      <div id='nco-dashboard'>
        <section>
          <div className='row'>
            <div className='small-12 columns'>
              <h3>Overview for {this.props.region.name}</h3>
            </div>
          </div>
          <div className='row'>
            <div className='medium-6 columns'>

            {caregiver_donut}
            </div>
          </div>
        </section>
      </div>
    );
  }
});

module.exports = NCODashboard;
