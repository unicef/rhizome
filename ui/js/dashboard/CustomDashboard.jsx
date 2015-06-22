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

    case 'PieChart':
      opts.margin = {
        top    : 0,
        right  : 80,
        bottom : 0,
        left   : 0
      };

      break;

    default:
      break;
  }

  return opts;
}

var CustomDashboard = React.createClass({
  propTypes : {
    editable      : React.PropTypes.bool,
    onAddChart    : React.PropTypes.func,
    onDeleteChart : React.PropTypes.func,
    onEditChart   : React.PropTypes.func,
  },

  getDefaultProps : function () {
    return {
      editable      : false,
      onAddChart    : _.noop,
      onDeleteChart : _.noop,
      onEditChart   : _.noop,
    };
  },

  render : function () {
    var numCharts = this.props.dashboard.charts.length;

    var data     = this.props.data;
    var loading  = this.props.loading;
    var campaign = this.props.campaign;
    var editable = this.props.editable;

    var charts = _.map(this.props.dashboard.charts, (chart, i) => {
      var title  = chart.title;
      var key    = _.get(chart, 'id', _.kebabCase(title));
      var id     = _.get(chart, 'id', _.camelCase(title));
      var series = data[id];
      var cols   = chart.type === 'BarChart' ?
        'small-10 end columns' :
        'medium-4 large-3 columns end';

      var options = getOptions(chart, campaign, data);

      var controls;
      if (editable) {
        controls = (
          <div className='button-bar' style={{float : 'right'}}>
            <a role='button' onClick={this.props.onDeleteChart.bind(null, i)}>
              <i className='fa fa-icon fa-trash fa-fw'></i>
            </a>
            <a role='button' onClick={this.props.onEditChart.bind(null, i)}>
              <i className='fa fa-icon fa-pencil fa-fw'></i>
            </a>
          </div>
        );
      }

      return (
        <div key={key} className={cols} style={{ paddingBottom: '1.5rem' }}>
          <h4>{title}{controls}</h4>
          <Chart type={chart.type} data={series} options={options}
            loading={loading} />
        </div>
      );
    });

    var addChart;
    if (editable) {
      addChart = (
        <div className='medium-4 large-3 columns end'>
          <a role='button' onClick={this.props.onAddChart}
            style={{whiteSpace:'nowrap', width:'100%', height:'100%'}}>
            <i className='fa fa-icon fa-fw fa-plus'></i>&ensp;Add Chart
          </a>
        </div>
      );
    }

    return (
      <div className='row'>{charts}{addChart}</div>
    );
  },
});

module.exports = CustomDashboard;
