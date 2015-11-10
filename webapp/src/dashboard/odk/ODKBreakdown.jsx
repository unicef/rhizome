'use strict'

var _     = require('lodash')
var React = require('react')

var Chart      = require('component/Chart.jsx')
var DonutChart = require('component/DonutChart.jsx')
var ToggleableStackedBar = require('dashboard/ToggleableStackedBar.jsx')

function prep (data) {
  return _(data)
    .groupBy('location.id')
    .filter(v => _(v).pluck('value').some(_.isFinite))
    .flatten()
    .groupBy('indicator.short_name')
    .map((v, n) => { return { name : n, values : v }; })
    .value()
}

var ODKBreakdown = React.createClass({
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
    var loading    = this.props.loading
    var data       = this.props.data

    var options = {
      x : _.property('value'),
      y : _.property('location.name'),
      margin : {
        top    : 0,
        right  : 80,
        bottom : 18,
        left   : 80
      }
    }

    return <div>
        <div className='row'>
          <div className='small-6 columns'>
            <h3>VCM Summary</h3>
                <ToggleableStackedBar
                  title='Missed Children'
                  loading={loading}
                  options={options}
                  data={prep(data.missedChildren)}
               />
          </div>
          <div className='small-6 columns'>
            <h3>Health Camps</h3>
            <ToggleableStackedBar
              title='Missed Children'
              loading={loading}
              options={options}
              data={prep(data.missedChildren)}
           />
          </div>
      </div>
      <div className='row'>
        <div className='small-6 columns'>
          <h3>Birth Tracking</h3>
          <ToggleableStackedBar
            title='Missed Children'
            loading={loading}
            options={options}
            data={prep(data.missedChildren)}
         />
        </div>
        <div className='small-6 columns'>
          <h3>Supportive Supervision</h3>
          <ToggleableStackedBar
            title='Missed Children'
            loading={loading}
            options={options}
            data={prep(data.missedChildren)}
         />
        </div>
    </div>
    </div>
  }
})

module.exports = ODKBreakdown
