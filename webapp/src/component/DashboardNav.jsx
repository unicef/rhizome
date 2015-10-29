'use strict';

var _ = require('lodash');
var React = require('react');


module.exports = React.createClass({
  render: function () {
    return (
      <ul className="dashboards-nav">
        <li>
          <a href="#">View My Dashboards</a>
          <ul className="dashboard-menu">
            <li>
              <a href="asdf">asdf</a>
            </li>
            <li>
              <a href="asdf">asdf</a>
            </li>
            <li>
              <a href="asdf">asdf</a>
            </li>
            <li>
              <a href="asdf">asdf</a>
            </li>
            <li>
              <a href="asdf">asdf</a>
            </li>
          </ul>
        </li>
        <li>
          <a href="/datapoints/dashboards/edit">Create a dashboard</a>
        </li>
      </ul>

    );
  },

});