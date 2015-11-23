import _ from 'lodash'
import d3 from 'd3'
import React from 'react'
import moment from 'moment'

import Chart from 'component/Chart.jsx'
import ChartUtil from '../utils/ChartUtil.js'

var ImmunityGap = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    data: React.PropTypes.array.isRequired,
    loading: React.PropTypes.bool
  },

  render: function () {
    var loading = this.props.loading

    var immunityGapData = ChartUtil.prepareUnderImmunizedData({
      data: this.props.data,
      campaign: this.props.campaign
    })

    var sumData = []

    if (immunityGapData.data.length > 1) {
      sumData = immunityGapData.data[0].values.map((d, i) => {
        return d.value + immunityGapData.data[1].values[i].value
      })
    }

    var maxRange = 1
    if (!_.isEmpty(sumData)) {
      maxRange = _.ceil(_.max(sumData), 1)
      if (Math.round(maxRange * 100) % 4 !== 0) {
        maxRange = _.ceil(maxRange + 0.1, 1)
      }
    }

    return (
      <div>
        <h4>Under immunized children</h4>
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
            yFormat: d3.format('%'),
            range: _.constant([0, maxRange])
          }} />
      </div>
    )
  }
})

export default ImmunityGap
