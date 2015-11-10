'use strict'

var _ = require('lodash')
var d3 = require('d3')
var React = require('react')

var DonutChart = require('component/DonutChart.jsx')

var indicatorForCampaign = function (campaign, indicator) {
  return d => d.campaign.id === campaign && d.indicator.id === indicator
}

var SocialData = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,
    data: React.PropTypes.object
  },

  render: function () {
    var campaign = this.props.campaign
    var loading = this.props.loading

    var data = _.filter(this.props.data,
        d => d.campaign.id === campaign.id && _.isFinite(d.value))

    var social = _.find(data, indicatorForCampaign(campaign.id, 28))
    var microplans = _.find(data, indicatorForCampaign(campaign.id, 27))

    var num = _.get(social, 'value')
    var den = _.get(microplans, 'value')

    var microText = ''
    var socialData

    if (_.isFinite(num) && _.isFinite(den)) {
      microText = num + ' / ' + den + ' microplans incorporate social data'
      socialData = [{value: num / den}]
    }

    var planLabel = function (d) {
      var fmt = d3.format('%')
      var v = _.get(d, '[0].value', '')
      return fmt(v)
    }

    return (
      <div className='row'>
        <div className='medium-4 columns'>
          <DonutChart data={socialData} label={planLabel}
                      loading={loading}
                      options={{
                innerRadius : 0.3,
                outerRadius : 0.5,
                domain      : _.constant([0, 1])
              }}/>
        </div>
        <div className='medium-4 columns'>
          {microText}
        </div>
      </div>
    )
  }
})

module.exports = SocialData
