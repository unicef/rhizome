'use strict';

var _     = require('lodash');
var React = require('react');
var moment = require('moment');

var Chart = require('component/Chart.jsx');

function _domain(data) {
  var lower = _(data)
    .pluck('indicator.bound_json')
    .flatten()
    .pluck('mn_val')
    .uniq()
    .filter(_.isFinite)
    .min();

  var upper = _(data)
    .pluck('indicator.bound_json')
    .flatten()
    .pluck('mx_val')
    .uniq()
    .filter(_.isFinite)
    .max();

  return [Math.min(lower, 0), Math.max(upper, _(data).flatten().pluck('value').max(), 1)];
}

function _matchCampaign(datapoint, campaign) {
  return _.result(datapoint, 'campaign.start_date.getTime') ===
    moment(campaign.start_date, 'YYYY-MM-DD').valueOf();
}

function _value(data, campaign) {
  return _.get(
    _(data)
      .filter(_.partial(_matchCampaign, _, campaign))
      .first(),
    'value');
}

function _marker(data, campaign) {
  var hx = _(data)
    .reject(_.partial(_matchCampaign, _, campaign))
    .pluck('value')
    .filter(_.isFinite)
    .value();

  return _.sum(hx) / hx.length;
}

function _targetRanges(indicator) {
  var targets = _(indicator.bound_json)
    .map(function (bound) {
      var lower = _.isFinite(bound.mn_val) ? bound.mn_val : -Infinity;
      var upper = _.isFinite(bound.mx_val) ? bound.mx_val : Infinity;

      return _.assign({}, bound, {
        mn_val : lower,
        mx_val : upper
      });
    })
    .filter(function (bound) {
      // FIXME: Temporary fix to filter out the "invalid" ranges
      return _.isFinite(bound.mn_val) && _.isFinite(bound.mx_val);
    })
    .sortBy('mn_val')
    .value();

  var boundaries = _(targets)
    .map(function (bound) {
      return [bound.mn_val, bound.mx_val]
    })
    .flatten()
    .uniq()
    .slice(1, -1)
    .value()

  return [_.pluck(targets, 'bound_name'), boundaries];
}

function _fill(data, campaign, targets) {
  var color = d3.scale.ordinal()
    .domain(['bad', 'ok', 'okay', 'good', ''])
    .range(['#AF373E', 'auto', 'auto', '#2B8CBE']);

  var scale = d3.scale.threshold()
    .domain(targets[1])
    .range(targets[0]);

  return color(scale(_value(data, campaign)));
}

module.exports = React.createClass({
  propTypes : {
    campaign   : React.PropTypes.object.isRequired,
    indicators : React.PropTypes.array.isRequired,

    cols       : React.PropTypes.number,
    data       : React.PropTypes.array,
    hideHelp   : React.PropTypes.func,
    showHelp   : React.PropTypes.func
  },

  getDefaultProps : function () {
    return {
      cols     : 1,
      hideHelp : _.noop,
      showHelp : _.noop,
    };
  },

  render : function () {
    var campaign = this.props.campaign;
    var showHelp = this.props.showHelp;
    var hideHelp = this.props.hideHelp;
    var data     = this.props.data;
    var loading  = this.props.loading;

    var charts = _(this.props.indicators)
      .map(function (indicator) {
        var targets = _targetRanges(indicator);

        var options = {
          domain     : _domain,
          value      : _.partial(_value, _, campaign),
          marker     : _.partial(_marker, _, campaign),
          y          : _.property('region'),
          width      : 154,
          height     : 51.3,
          fill       : _.partial(_fill, _, campaign, targets),
          format     : d3.format('%'),
          thresholds : targets[1],
          targets    : targets[0]
        };

        var title = indicator.short_name

        var chartData = _(data)
          .filter(d => d.indicator.id === indicator.id)
          .groupBy(options.y) // There could coneivably be multiple bars in the chart
          .values()
          .value();

        return (
          <li key={'bullet-chart-' + indicator.id}>
            <h6 onMouseEnter={_.partial(showHelp, indicator)} onMouseLeave={hideHelp}>{title}</h6>
            <Chart type='BulletChart' loading={loading} data={chartData} options={options} />
          </li>
        );
      })
      .value();

    return (<ul className={'small-block-grid-' + this.props.cols}>{charts}</ul>);
  },
});
