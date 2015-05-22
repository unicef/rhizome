'use strict';

var _      = require('lodash');
var moment = require('moment');
var React  = require('react');

var YtDChart = require('./YtDChart.jsx');

module.exports = React.createClass({
  getDefaultProps : function () {
    return {
      data     : [],
      campaign : null,
      region   : null
    };
  },

  getInitialState : function () {
    return {
      totalCases : null,
      newCases   : null
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
    var year       = campaign.start_date.getFullYear();
    var month      = moment(campaign.start_date).format('MMM');
    var totalCases = null;
    var newCases   = null;

    if (campaign) {
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
          'color'       : '#2b8cbe',
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
      .range(['#2b8cbe', '#525b5e', '#82888e', '#98a0a8', '#b6c0cc'])
      .domain(_(this.props.data)
        .map(_.method('campaign.start_date.getFullYear'))
        .uniq()
        .sortBy()
        .reverse()
        .value());

    return (
      <div>
        {title}
        <div style={{ position : 'relative' }}>
          {newCaseLabel}
          <YtDChart id='polio-cases-ytd'
            data={this.props.data}
            getColor={_.flow(_.property('name'), color)}
            aspect={1.757} />
        </div>
      </div>
    )
  },

});
