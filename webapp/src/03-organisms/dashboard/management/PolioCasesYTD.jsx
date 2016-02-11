import _ from 'lodash'
import moment from 'moment'
import React from 'react'

import YTDChart from '02-molecules/YTDChart.jsx'

export default React.createClass({
  propTypes: {
    campaign: React.PropTypes.object,
    data: React.PropTypes.array,
    loading: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: false
    }
  },

  render: function () {
    var data = this.props.data
    var campaign = this.props.campaign
    var year = ''
    var totalCases = null
    var newCases = null
    var loading = this.props.loading

    if (campaign) {
      var m = moment(campaign.start_date, 'YYYY-MM-DD')
      year = m.format('YYYY')

      // Sum all of the reported Polio cases for the year
      totalCases = _(data)
        .filter(function (d) { return d.campaign.start_date.getFullYear().toString() === year })
        .pluck('value')
        .sum()

      // Find the number of reported cases for this campaign
      newCases = _.get(
        _.find(
          data,
          function (d) { return d.campaign.start_date.getTime() === m.valueOf() }),
        'value')
    }

    // Set the title based on whether there is data
    var title = _.isEmpty(data)
    ? (<h4>Wild Polio Cases</h4>)
    : (<h4 style={{'color': '#F15046'}}>
        {totalCases} Polio cases this year
      </h4>)

    if (!_.isFinite(newCases) || newCases < 0) {
      newCases = 0
    }
    var plural = newCases !== 1 ? 's' : ''
    var newCaseLabel = (<h4 style={{'color': '#F15046'}}>{newCases} new case{plural}</h4>)

    return (
      <div id='polio-cases-ytd'>
        {title}
        <div style={{ position: 'relative' }}>
          {newCaseLabel}
          <YTDChart id='polio-cases-ytd'
            data={data}
            loading={loading} />
        </div>
      </div>
    )
  }

})
