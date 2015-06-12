'use strict';

var _ = require('lodash');
var React = require('react');

/**
 * Convert the value of each datapoint to a percentage of the total value
 */
function percentage(dataset) {
  var total = _(dataset).pluck('value').sum();

  _.forEach(dataset, function (d) {
    d.value /= total;
  });

  return dataset;
}

var ImmunityGap = React.createClass({
  propTypes : {
    campaign : React.PropTypes.object,
    data     : React.PropTypes.array
  },

  render : function () {
    var data = _(data)
      .each(function (d) {
        // Add a property to each datapoint indicating the fiscal quarter
        d.quarter = moment(d.campaign.start_date).format('[Q]Q YYYY');
      })
      .groupBy(function (d) {
        return d.indicator + '-' + d.quarter;
      })
      .map(function (datapoints) {
        // Calculate the total number of children with X doses of OPV for
        // each quarter
        return _.assign({}, datapoints[0], {
          'value' : _(datapoints).pluck('value').sum()
        });
      })
      .groupBy('quarter')
      .map(percentage)
      .flatten()
      .reject(function (d) {
        // Exclude 4+ doses, because that is implied as 1 - <0 doses> - <1–3 doses>
        // jshint eqeqeq: false
        return d.indicator == '433';
      })
      .groupBy('indicator')
      .map(_.partialRight(seriesObject, indicators))
      .value();

    var stack = d3.layout.stack()
      .offset('zero')
      .values(function (d) { return d.values; })
      .x(function (d) { return d.campaign.start_date; })
      .y(function (d) { return d.value; });

    var color = _.flow(
      _.property('name'),
      d3.scale.ordinal()
        .domain(_(immunityGap).pluck('name').sortBy().value())
        .range(['#AF373E', '#FABAA2'])
    );

    var lower = start.clone()
      .startOf('quarter')
      .subtract(3, 'years');
    var upper = start.clone().endOf('quarter');

    var immunityScale = _.map(d3.time.scale()
        .domain([lower.valueOf(), upper.valueOf()])
        .ticks(d3.time.month, 3),
      _.method('getTime')
    );

    return (
      <div>
        <h4>Under-Immunized Children</h4>
        <Chart type='ColumnChart'
          data={stack(data)}
          options={{
            aspect  : 1.757,
            color   : color,
            domain  : _.constant(immunityScale),
            values  : _.property('values'),
            x       : function (d) { return moment(d.campaign.start_date).startOf('quarter').valueOf(); },
            xFormat : function (d) { return moment(d).format('[Q]Q [’]YY'); },
            y0      : _.property('y0'),
            yFormat : d3.format('%')
          }} />
      </div>
    );
  }
});

module.exports = ImmunityGap;
