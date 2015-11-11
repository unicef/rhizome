'use strict'

var _ = require('lodash')
var d3 = require('d3')
var moment = require('moment')
var React = require('react')

var Chart = require('component/Chart.jsx')

module.exports = React.createClass({
  propTypes: {
    data: React.PropTypes.array.isRequired,
    id: React.PropTypes.string,
    options: React.PropTypes.object
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: false
    }
  },

  render: function () {
    var series = _(this.props.data)
      .groupBy(_.method('campaign.start_date.getFullYear'))
      .map(function (values, year) {
        return {
          name: year,
          values: _(values)
            .groupBy(_.method('campaign.start_date.getMonth'))
            .map(function (d, month) {
              return {
                month: Number(month),
                value: _(d).pluck('value').sum()
              }
            })
            .sortBy('month')
            .transform(function (result, d) {
              var o = {
                month: d.month,
                year: year,
                value: d.value,
                x: moment({ M: d.month }).toDate(),
                total: _.get(_.last(result), 'total', 0) + _.get(d, 'value', 0)
              }

              result.push(o)

              return result
            })
            .value()
        }
      })
      .sortBy('name')
      .value()

    // Convert a 2-digit month number to a 3-character month name
    // var fmtMonth = function (d) { return moment(d, 'MM').format('MMM') }

    var props = _.merge({},
      _.omit(this.props, 'id', 'data'), {
        data: series,
        options: {
          domain: _.constant([moment({ M: 0 }).toDate(), moment({ M: 11 }).toDate()]),
          range: _.constant([0, _(series).pluck('values').flatten().pluck('total').max()]),
          x: _.property('x'),
          xFormat: d3.time.format('%b'),
          y: _.property('total')
        }
      })

    return (
      <Chart type='LineChart' {...props} />
    )
  }
})
