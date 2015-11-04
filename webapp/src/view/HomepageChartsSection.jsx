'use strict';

var React = require('react');
var HomepageCharts = require('dashboard/homepage/HomepageCharts.jsx');

var HomepageChartsSection = React.createClass({
    getManagementDashboardUrl: function() {
      var [year, month] = this.props.date.split('-');
      return `/datapoints/management-dashboard/${this.props.location}/${year}/${month}`;
    },

    getDistrictSummaryUrl: function() {
      var [year, month] = this.props.date.split('-');
      return `/datapoints/district-dashboard/${this.props.location}/${year}/${month}`;
    },

    getNGACampaignMonitoringUrl: function() {
      var [year, month] = this.props.date.split('-');
      return `/datapoints/nga-campaign-monitoring/${this.props.location}/${year}/${month}`;
    },


    render: function () {
        var dashboard = React.createElement(HomepageCharts, this.props.data);
        var chartId = `${this.props.location.toLowerCase()}-chart`;

        var controls;
        if(this.props.location === 'Nigeria') {
            controls =
              <div className="chart-button-group">
                <a href={this.getManagementDashboardUrl()}>
                  <div className="chart-button"><span>Country overview</span></div>
                </a>

                <a href={this.getDistrictSummaryUrl()}>
                  <div className="chart-button"><span>District summary</span></div>
                </a>

                <a href={this.getNGACampaignMonitoringUrl()}>
                  <div className="chart-button"><span>NGA Campaign Monitoring</span></div>
                </a>
              </div>
        } else {
            controls =
              <div className="chart-button-group">
                <a href={this.getManagementDashboardUrl()}>
                  <div className="chart-button"><span>Country overview</span></div>
                </a>
                <a href={this.getDistrictSummaryUrl()}>
                  <div className="chart-button"><span>District summary</span></div>
                </a>
              </div>
        }

        return (
            <div>
                <div className="large-4 columns chart-container" id={chartId}>
                    <div className="chart">
                        <h5>{this.props.location}</h5>
                        {dashboard}
                        {controls}
                    </div>
                </div>

            </div>
        );
    }
});

module.exports = HomepageChartsSection;
