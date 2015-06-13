'use strict';

var _     = require('lodash');
var React = require('react');

var PolioCasesYTD = require('dashboard/management/PolioCasesYTD.jsx');
var ImmunityGap   = require('dashboard/management/ImmunityGap.jsx');

var Impact = React.createClass({

  render : function () {
    var cases = _.filter(this.props.data, function (d) {
      return d.indicator.id === 168;
    });

    var immunity = _.filter(this.props.data, function (d) {
      return [431,432,433].indexOf(d.indicator.id) > -1;
    });

    var campaign = this.props.campaign;

    return (
      <div className='medium-2 columns'>
        <h3>Impact</h3>
        <PolioCasesYTD data={cases} campaign={campaign} />
        <ImmunityGap data={immunity} campaign={campaign} />
      </div>
    );
  },
});

module.exports = Impact;
