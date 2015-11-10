'use strict'

var _ = require('lodash')
var d3 = require('d3')
var React = require('react')

var Chart = require('component/Chart.jsx')
var DonutChart = require('component/DonutChart.jsx')
var Monitoring = require('dashboard/nco/Monitoring.jsx')

function donutLabel (data, labelText) { // FIXME this is repeated in nco/overview
  var value = _.get(data, '[0].value')

  if (!_.isFinite(value)) {
    return
  }

  var fmt = d3.format('%')
  var label

  if (labelText) {
    label = (<span><br /><label>{labelText}</label></span>)
  }

  return (<span>{fmt(value)}{label}</span>)
}

var ODKOverview = React.createClass({
  propTypes : {
    data : React.PropTypes.object.isRequired,
    loading : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    }
  },

  render : function () {
    var loading = this.props.loading
    var data = this.props.data

    var options = {
      innerRadius : 0.6,
      domain      : _.constant([0, 1]),
      labelStyle  : {
        lineHeight : 1
      }
    }

    var data_coverage_donut = <div>
        <div className='small-12 columns'>
          <h4 style={{ textAlign : 'center' }}>Caregiver Awareness</h4>
        </div>

        <div className='medium-6 push-3 end columns'>
          <DonutChart
            loading={loading}
            data={data.caregiverAwareness}
            label={donutLabel}
            options={options} />
        </div>
      </div>
    return <div>
      <div>{data_coverage_donut}</div>
    </div>
  }
})

module.exports = ODKOverview
