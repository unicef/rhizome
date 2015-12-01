import _ from 'lodash'
import d3 from 'd3'
import Layer from 'react-layer'
import React from 'react'
import moment from 'moment'

import Chart from 'component/Chart.jsx'
import Tooltip from 'component/Tooltip.jsx'

function _domain (data) {
  var lower = _(data)
    .pluck('indicator.bound_json')
    .flatten()
    .pluck('mn_val')
    .uniq()
    .filter(_.isFinite)
    .min()

  var upper = _(data)
    .pluck('indicator.bound_json')
    .flatten()
    .pluck('mx_val')
    .uniq()
    .filter(_.isFinite)
    .max()

  return [Math.min(lower, 0), Math.max(upper, _(data).flatten().pluck('value').max(), 1)]
}

function _matchCampaign (datapoint, campaign) {
  return _.result(datapoint, 'campaign.start_date.getTime') ===
    moment(campaign.start_date, 'YYYY-MM-DD').valueOf()
}

function _value (data, campaign) {
  return _.get(
    _(data)
      .filter(_.partial(_matchCampaign, _, campaign))
      .first(),
    'value')
}

function _marker (data, campaign) {
  var hx = _(data)
    .reject(_.partial(_matchCampaign, _, campaign))
    .pluck('value')
    .filter(_.isFinite)
    .value()

  return _.sum(hx) / hx.length
}

function _targetRanges (indicator) {
  var targets = _(_.get(indicator, 'bound_json'))
    .map(function (bound) {
      var lower = _.isFinite(bound.mn_val) ? bound.mn_val : -Infinity
      var upper = _.isFinite(bound.mx_val) ? bound.mx_val : Infinity

      return _.assign({}, bound, {
        mn_val: lower,
        mx_val: upper
      })
    })
    .filter(function (bound) {
      // FIXME: Temporary fix to filter out the 'invalid' ranges
      return _.isFinite(bound.mn_val) && _.isFinite(bound.mx_val)
    })
    .sortBy('mn_val')
    .value()

  var boundaries = _(targets)
    .map(function (bound) {
      return [bound.mn_val, bound.mx_val]
    })
    .flatten()
    .uniq()
    .slice(1, -1)
    .value()

  return [_.pluck(targets, 'bound_name'), boundaries]
}

function _fill (data, campaign, targets, colorRange) {
  var color = d3.scale.ordinal()
    .domain(['bad', 'ok', 'good'])
    .range(colorRange)

  var scale = d3.scale.threshold()
    .domain(targets[1])
    .range(targets[0])

  return color(scale(_value(data, campaign)))
}

function _valueText (value, targets) {
  var threshold = targets[1]
  var target = targets[0]
  if (!_.isNull(value) && _.isFinite(value)) {
    if (value < threshold[0]) {
      return target[0]
    } else if (value >= threshold[0] && value < threshold[1]) {
      return target[1]
    } else {
      return target[2]
    }
  }
  return ''
}

export default React.createClass({
  propTypes: {
    campaign: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.array.isRequired,
    loading: React.PropTypes.bool,
    cols: React.PropTypes.number,
    data: React.PropTypes.array
  },

  getDefaultProps: function () {
    return {
      cols: 1
    }
  },

  render: function () {
    var campaign = this.props.campaign
    var data = this.props.data
    var loading = this.props.loading
    var dataColorRange = ['#DB5344', '#79909F', '#2FB0D3']
    var xAxisColorRange = ['#F8DDDB', '#B6D0D4', '#A1C3C6']
    var noDataColor = '#B9C3CB'
    let isBulletChart = true

    var charts = _(this.props.indicators)
      .map((indicator, i) => {
        var targets = _targetRanges(indicator)

        var options = {
          domain: _domain,
          value: _.partial(_value, _, campaign),
          marker: _.partial(_marker, _, campaign),
          y: _.property('location'),
          width: 154,
          height: 10,
          dataFill: _.partial(_fill, _, campaign, targets, dataColorRange),
          axisFill: _.partial(_fill, _, campaign, targets, xAxisColorRange),
          format: d3.format('%'),
          thresholds: targets[1],
          targets: targets[0],
          valueText: _.partial(_valueText, _, targets)
        }

        var chartData = _(data)
          .filter(d => d.indicator.id === indicator.id)
          .groupBy(options.y) // There could coneivably be multiple bars in the chart
          .values()
          .value()

        var title = _.get(indicator, 'short_name')
        var threshold = d3.scale.threshold().domain(options.thresholds).range(dataColorRange)
        var titleColor = options.value(chartData[0]) ? threshold(options.value(chartData[0])) : noDataColor

        return (
          <li key={'bullet-chart-' + _.get(indicator, 'id', i)}>
            <h6 onMouseMove={this._showHelp.bind(this, indicator)} onMouseLeave={this._hideHelp} style={{color: titleColor}}>
              {title}
            </h6>
            <Chart type='BulletChart' loading={loading} data={chartData} options={options} isBulletChart={isBulletChart}/>
          </li>
        )
      })
      .value()

    return (<ul className={'small-block-grid-' + this.props.cols}>{charts}</ul>)
  },

  _showHelp: function (indicator, evt) {
    var render = function () {
      return (
        <Tooltip left={evt.pageX} top={evt.pageY}>
          <h3>{indicator.name}</h3>

          <p>{indicator.description}</p>
        </Tooltip>
      )
    }

    if (this.layer) {
      this.layer._render = render
    } else {
      this.layer = new Layer(document.body, render)
    }

    this.layer.render()
  },

  _hideHelp: function () {
    if (this.layer) {
      this.layer.destroy()
      this.layer = null
    }
  }
})
