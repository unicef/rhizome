'use strict';

var _ = require('lodash');
var React = require('react');

var Chart = require('component/Chart.jsx');

function getOptions(chart) {
  var opts = {};

  switch (chart.type) {
    case 'ScatterChart':
      opts.x = _.property('[' + chart.indicators[0] + ']');
      opts.y = _.property('[' + chart.indicators[1] + ']');
      break;

    case 'ChoroplethMap':
      opts.value = _.property('.properties[' + chart.indicators[0] + ']');
      break;

    default:
      break;
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

    var data    = this.props.data;
    var loading = this.props.loading;

    var charts = _.map(this.props.dashboard.charts, function (chart) {
      var title  = chart.title;
      var key    = _.get(chart, 'id', _.kebabCase(title));
      var id     = _.get(chart, 'id', _.camelCase(title));
      var series = data[id];
      var cols;

      switch (chart.type) {
        case 'BarChart':
          cols = 'small-10 end columns';
          break;

        default:
          cols = numCharts < 2 ? 'small-12 columns' : 'medium-4 large-3 columns end';
          break;
      }

      if (chart.type === 'Bar')

      var options = getOptions(chart);

      return (
        <div key={key} className={cols} style={{ paddingBottom: '1.5rem' }}>
          <h4>{title}</h4>
          <Chart type={chart.type} data={series} options={options} loading={loading} />
        </div>
      );
    });

    return (
      <div className='row'>{charts}</div>
    );
  },
});

module.exports = CustomDashboard;
