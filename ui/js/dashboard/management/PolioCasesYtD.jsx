'use strict';

var _      = require('lodash');
var moment = require('moment');
var React  = require('react');

var YtDChart = require('component/YtDChart.jsx');

module.exports = React.createClass({
  propTypes : {
    campaign : React.PropTypes.object,
    data     : React.PropTypes.array,
  },

  getDefaultProps : function () {
    return {
      data     : [],
    };
  },

  render : function () {
    var campaign   = this.props.campaign;
    var year       = '';
    var month      = '';
    var totalCases = null;
    var newCases   = null;

    if (campaign) {
      var m = moment(campaign.start_date, 'YYYY-MM-DD');
      year  = m.format('YYYY');
      month = m.format('MMM');

      // Sum all of the reported Polio cases for the year
      totalCases = _(this.props.data)
        .filter(function (d) { return d.campaign.start_date.getFullYear() == year; })
        .pluck('value')
        .sum();

      // Find the number of reported cases for this campaign
      newCases = _.get(
        _.find(
          this.props.data,
          function (d) { return d.campaign.start_date.getTime() === m.valueOf();}),
        'value');
    }

    // Set the title based on whether there is data
    var title = _.isEmpty(this.props.data) ?
      (<h4>Polio Cases</h4>) :
      (<h4>
        Polio cases in {year} (as of {month}):&ensp;<span
        style={{
          'color'       : '#AF373E',
          'fontWeight' : 'bold'
        }}>{totalCases}</span>
      </h4>);

    var newCaseLabel = '';

    if (_.isFinite(newCases) && newCases > 0) {
      var plural = newCases !== 1 ? 's' : '';
      newCaseLabel = (
        <div id='new-polio-cases'
          style={{
            position :'absolute'
          }}>{newCases} new case{plural}</div>
      );
    }

    var color = d3.scale.ordinal()
      .range(['#AF373E', '#525b5e', '#82888e', '#98a0a8', '#b6c0cc'])
      .domain(_(this.props.data)
        .map(_.method('campaign.start_date.getFullYear'))
        .uniq()
        .sortBy()
        .reverse()
        .value());

    return (
      <section id='polio-cases-ytd'>
        {title}
        <div style={{ position : 'relative' }}>
          {newCaseLabel}
          <YtDChart id='polio-cases-ytd'
            data={this.props.data}
            options={{
              color  : _.flow(_.property('name'), color),
              aspect : 1.757
            }} />
        </div>
      </section>
    )
  },

});
