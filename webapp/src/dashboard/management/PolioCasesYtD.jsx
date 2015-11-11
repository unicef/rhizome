'use strict'

var _ = require('lodash')
var moment = require('moment')
var React = require('react')

var YtDChart = require('component/YtDChart.jsx')

module.exports = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object,
    data: React.PropTypes.array
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: false
    }
  },

  render: function () {
    var campaign = this.props.campaign
    var year = ''
    var totalCases = null
    var newCases = null
    var loading = this.props.loading
    var month = null

    if (campaign) {
      var m = moment(campaign.start_date, 'YYYY-MM-DD')
      year = m.format('YYYY')
      month = m.format('MMM')

      // Sum all of the reported Polio cases for the year
      totalCases = _(this.props.data)
        .filter(function (d) { return d.campaign.start_date.getFullYear() === year })
        .pluck('value')
        .sum()

      // Find the number of reported cases for this campaign
      newCases = _.get(
        _.find(
          this.props.data,
          function (d) { return d.campaign.start_date.getTime() === m.valueOf() }),
        'value')
    }

    // Set the title based on whether there is data
    var title = _.isEmpty(this.props.data)
    ? (<h4>Wild Polio Cases</h4>)
    : (<h4 style={{'color': '#F15046'}}>
        {totalCases} Polio cases this year
      </h4>)

    var newCaseLabel = ''

    if (_.isFinite(newCases) && newCases > 0) {
      var plural = newCases !== 1 ? 's' : ''
      newCaseLabel = (
        <div id='new-polio-cases'>{newCases} new case{plural}</div>
      )
    }

    return (
      <div id='polio-cases-ytd'>
        {title}
        <div style={{ position: 'relative' }}>
          {newCaseLabel}
          <YtDChart id='polio-cases-ytd'
            data={this.props.data}
            loading={loading}
            options={{
              aspect: 2.26
            }} />
        </div>
      </div>
    )
  }

})
