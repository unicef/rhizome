'use strict'

var _ = require('lodash')
var d3 = require('d3')
var React = require('react')
var moment = require('moment')

var Chart = require('component/Chart.jsx')
var ChartUtil = require('../utils/ChartUtil.js')

var ImmunityGap = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    data: React.PropTypes.array.isRequired
  },

  render: function () {
    var loading = this.props.loading

    var immunityGapData = ChartUtil.prepareUnderImmunizedData({
      data: this.props.data,
      campaign: this.props.campaign
    })

    return (
      <div>
        <h4>Under-Immunized Children</h4>
        <Chart type='ColumnChart'
          data={immunityGapData.data}
          loading={loading}
          options={{
            aspect: 2.26,
            color: immunityGapData.color,
            domain: _.constant(immunityGapData.immunityScale),
            values: _.property('values'),
            x: function (d) { return moment(d.campaign.start_date).startOf('quarter').valueOf() },
            xFormat: function (d) { return moment(d).format('[Q]Q [ ]YYYY') },
            y0: _.property('y0'),
            yFormat: d3.format(',%')
          }} />
      </div>
    )
  }
})

module.exports = ImmunityGap
