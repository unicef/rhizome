'use strict';

var _ = require('lodash');
var React = require('react');

module.exports = React.createClass({

  render: function () {

    return (
      <ul className="dashboards-nav">
        <li className="medium-6 columns">
          <a href="#">View My Dashboards</a>
          <ul className="dashboard-menu">
            <li>
              <a href="/datapoints/management-dashboard">Management Dashboard</a>
            </li>
            <li>
              <a href="/datapoints/district-dashboard">District Dashboard</a>
            </li>
            <li>
              <a href="/datapoints/nga-campaign-monitoring">NGA Campaign Monitoring</a>
            </li>
            <li>
              <a href="/datapoints/odk-dashboard">ODK Dashboard</a>
            </li>
            <li>
                <a href="/datapoints/dashboards">See all custom dashboards</a>
            </li>
          </ul>
        </li>
        <li className="medium-6 columns">
          <a href="/datapoints/dashboards/edit">Create a dashboard</a>
        </li>
      </ul>

    );
  }

});
