'use strict';

var _ = require('lodash');
var React = require('react');

var Chart = require('component/Chart.jsx');

function getOptions(chart) {
  var opts = {};

  if (chart.type === 'ScatterChart') {
    opts.x = _.property('[' + chart.indicators[0] + ']');
    opts.y = _.property('[' + chart.indicators[1] + ']');
  }

  return opts;
}

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

    var data    = this.props.data;
    var loading = this.props.loading;

    var charts = _.map(this.props.dashboard.charts, function (chart) {
      var title  = chart.title;
      var key    = _.get(chart, 'id', _.kebabCase(title));
      var id     = _.get(chart, 'id', _.camelCase(title));
      var series = data[id];

      var options = getOptions(chart);

      return (
        <li key={key}>
          <h4>{title}</h4>
          <Chart type={chart.type} data={series} options={options} loading={loading} />
        </li>
      );
    });

    return (
      <div className='row'>
        <div className='small-12 columns'>
          <ul className={blockGrid}>{charts}</ul>
        </div>
      </div>
    );
  },
});

module.exports = CustomDashboard;
