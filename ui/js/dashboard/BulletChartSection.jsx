'use strict';

var _     = require('lodash');
var React = require('react');

var Chart = require('component/Chart.jsx');

function _domain(data) {
  var lower = _(data)
    .pluck('indicator.indicator_bounds')
    .flatten()
    .pluck('mn_val')
    .uniq()
    .filter(_.isFinite)
    .min();

  var upper = _(data)
    .pluck('indicator.indicator_bounds')
    .flatten()
    .pluck('mx_val')
    .uniq()
    .filter(_.isFinite)
    .max();

  return [Math.min(lower, 0), Math.max(upper, _(data).pluck('value').max(), 1)];
}

function _matchCampaign(datapoint, campaign) {
  return _.result(datapoint, 'campaign.start_date.getTime') ===
    _.result(campaign, 'start_date.getTime');
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

function _targetRanges(data) {
  var targets = _(data)
    .pluck('indicator.indicator_bounds')
    .flatten()
    .indexBy('bound_name')
    .values()
    .filter(function (bound) {
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
    campaign : React.PropTypes.object.isRequired,
    data     : React.PropTypes.array.isRequired,
  },

  render : function () {
    var campaign = this.props.campaign;

    var charts = _(this.props.data)
      .groupBy('indicator.id')
      .map(function (data, indicator) {
        var targets = _targetRanges(data);

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
          targets    : targets[0],
          fontSize   : 12
        };

        var title = _.get(data, '[0].indicator.short_name', '');

        return (
          <li key={'bullet-chart-' + indicator}>
            <h6>{title}</h6>
            <Chart type='BulletChart'
              data={_(data).groupBy(options.y).values().value()}
              options={options} />
          </li>
        );
      })
      .value();

    return (<ul className='small-block-grid-2'>{charts}</ul>);
  }
});
