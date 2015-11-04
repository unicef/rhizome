'use strict';

var _ = require('lodash');
var React = require('react');

var HomepageChartsSection = require('view/HomepageChartsSection.jsx');

var HomepageChartsView = React.createClass({
    render: function () {
      return (
          <div>
            <HomepageChartsSection location="Afghanistan" date="2014-01" dashboard="homepage-afghanistan"/>
            <HomepageChartsSection location="Pakistan" date="2014-01" dashboard="homepage-pakistan"/>
            <HomepageChartsSection location="Nigeria" date="2014-01" dashboard="homepage-nigeria"/>
          </div>
      );
    }
});

module.exports = HomepageChartsView;
