'use strict';

var _      = require('lodash');
var moment = require('moment');
var React  = require('react');

var YtDChart = require('component/YtDChart.jsx');

module.exports = React.createClass({
  getDefaultProps : function () {
    return {
      data     : [],
      campaign : null,
      region   : null
    };
  },

  shouldComponentUpdate : function (nextProps) {
    // Update if we have a campaign and region, and the campaign or region is
    // different. If this condition is false, it shouldn't be the case that the
    // new cases or total cases has changed, so we don't need to check that.
    return !(_.isNull(nextProps.campaign) || _.isNull(nextProps.region)) &&
      (nextProps.campaign.id !== _.get(this.props, 'campaign.id') ||
      nextProps.region.id !== _.get(this.props, 'region.id'));
  },

  render : function () {
    var campaign   = this.props.campaign;
    var year       = '';
    var month      = '';
    var totalCases = null;
    var newCases   = null;

    if (campaign) {
      year  = campaign.start_date.getFullYear();
      month = moment(campaign.start_date).format('MMM');

      // Sum all of the reported Polio cases for the year
      totalCases = _(this.props.data)
        .filter(function (d) { return d.campaign.start_date.getFullYear() === year; })
        .pluck('value')
        .sum();

      // Find the number of reported cases for this campaign
      newCases = _.get(
        _.find(
          this.props.data,
          function (d) { return d.campaign.start_date.getTime() === campaign.start_date.getTime();}),
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
