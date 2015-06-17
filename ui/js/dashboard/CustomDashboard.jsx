'use strict';

var _ = require('lodash');
var React = require('react');

var Chart = require('component/Chart.jsx');

var CustomDashboard = React.createClass({
  propTypes : {
    editable : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      editable : false
    };
  },

  render : function () {
    var numCharts = this.props.dashboard.charts.length;
    var blockGrid = 'medium-block-grid-' + Math.min(numCharts, 3) +
      ' large-block-grid-' + Math.min(numCharts, 4);
    var data = this.props.data;

    var charts = _.map(this.props.dashboard.charts, function (chart) {
      var title  = chart.title;
      var key    = _.get(chart, 'id', _.kebabCase(title));
      var id     = _.get(chart, 'id', _.camelCase(title));
      var series = data[id];

      if (!_.isEmpty(chart.series)) {
        series = _(series).groupBy(chart.series).map((v, k) => {
          return { name : k, values : v};
        }).value();
      }

      return (
        <li key={key}>
          <h4>{title}</h4>
          <Chart type={chart.type} data={series} />
        </li>
      );
    });

    return (
      <ul className={blockGrid}>{charts}</ul>
    );
  },
});

module.exports = CustomDashboard;
