'use strict';

var _ = require('lodash');
var d3 = require('d3');
var React = require('react');
var moment = require('moment');

var Chart = require('component/Chart.jsx');

function getOptions(chart, campaign, data) {
  var opts = {};

  switch (chart.type) {
    case 'ScatterChart':
      opts.x = _.property('[' + chart.indicators[0] + ']');
      opts.y = _.property('[' + chart.indicators[1] + ']');
      break;

    case 'ChoroplethMap':
      opts.value = _.property('.properties[' + chart.indicators[0] + ']');
      break;

    case 'ColumnChart':
      var upper = moment(campaign.start_date);
      var lower = upper.clone().subtract(chart.timeRange);

      opts.domain = _.constant(_.map(d3.time.scale()
            .domain([lower.valueOf(), upper.valueOf()])
            .ticks(d3.time.month, 1),
          _.method('getTime')
        ));

      opts.x = d => moment(d.campaign.start_date).valueOf();
      opts.xFormat = d => moment(d).format('MMM YY');
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

    var data     = this.props.data;
    var loading  = this.props.loading;
    var campaign = this.props.campaign;

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

      var options = getOptions(chart, campaign, data);

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
