import React from 'react'
import HomepageCharts from 'dashboard/homepage/HomepageCharts.jsx'

var HomepageChartsSection = React.createClass({
  propTypes: {
    location: React.PropTypes.string,
    data: React.PropTypes.object
  },
  getManagementDashboardUrl: function () {
    var [year, month] = this.props.data.campaign.start_date.split('-')
    return `/datapoints/management-dashboard/${this.props.location}/${year}/${month}`
  },

  getDistrictSummaryUrl: function () {
    var [year, month] = this.props.data.campaign.start_date.split('-')
    return `/datapoints/district-dashboard/${this.props.location}/${year}/${month}`
  },

  getNGACampaignMonitoringUrl: function () {
    var [year, month] = this.props.data.campaign.start_date.split('-')
    return `/datapoints/nga-campaign-monitoring/${this.props.location}/${year}/${month}`
  },

  render: function () {
    var dashboard = React.createElement(HomepageCharts, this.props.data)
    var chartId = `${this.props.location.toLowerCase()}-chart`

    var controls
    if (this.props.location === 'Nigeria') {
      controls =
        <div className='chart-button-group'>
        <a href={this.getManagementDashboardUrl()} className='chart-button small-4 columns'>
          Country<br />overview
        </a>

        <a href={this.getDistrictSummaryUrl()} className='chart-button small-4 columns'>
          District<br />summary
        </a>

        <a href={this.getNGACampaignMonitoringUrl()} className='chart-button chart__button--response small-4 columns'>
          NGA Campaign<br />Monitoring
        </a>
        </div>
    } else {
      controls =
        <dev className='chart-button-group'>
        <a href={this.getManagementDashboardUrl()} className='chart-button small-6 columns'>
          Country<br />overview
        </a>
        <a href={this.getDistrictSummaryUrl()} className='chart-button small-6 columns'>
          District<br />summary
        </a>
        </dev>
    }

    return (
      <div>
        <div className='large-4 columns chart-container' id={chartId}>
          <div className='chart'>
            <h5>{this.props.location}</h5>
            {dashboard}
            {controls}
          </div>
        </div>
      </div>
    )
  }
})

export default HomepageChartsSection
