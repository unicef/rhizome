import _ from 'lodash'
import React from 'react'
import moment from 'moment'


var EocPreCampaign = React.createClass({

  propTypes: {
    dashboard: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,

    campaign: React.PropTypes.object,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool,
    location: React.PropTypes.object
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: true
    }
  },

  render: function () {
    console.log('somethign should be loading')
    // var campaign = this.props.campaign
    // var printDate = moment(campaign.start_date).format('MMM ‘YY')
    // var data = this.props.data
    // var indicators = _.indexBy(this.props.indicators, 'id')
    // var loading = this.props.loading
    // var location = _.get(this.props, 'location.name', '')
    // var dashboardName = 'EOC Pre Campaig Dashboard'.toUpperCase()
    //
    // var charts = this.props.dashboard.charts
    //   .groupBy('section')
    //   .transform(function (result, charts, sectionName) {
    //     var section = {}
    //     _.each(charts, (c, i) => {
    //       section[_.camelCase(_.get(c, 'title', i))] = _.map(c.indicators, ind => indicators[ind])
    //     })
    //     result[sectionName] = section
    //   })
    //   .value()

    return (
      <div id='eoc-pre-campaign-dashboard'>
      </div>
    )
  }
})

export default EocPreCampaign
