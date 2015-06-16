'use strict';

var _     = require('lodash');
var React = require('react');

var PolioCasesYTD = require('dashboard/management/PolioCasesYTD.jsx');
var ImmunityGap   = require('dashboard/management/ImmunityGap.jsx');

var Impact = React.createClass({

  propTypes : {
    campaign : React.PropTypes.object,
    data     : React.PropTypes.object,
  },

  render : function () {
    var data     = this.props.data;
    var campaign = this.props.campaign;

    return (
      <div className='medium-2 columns'>
        <h3>Impact</h3>
        <PolioCasesYTD data={data.polioCasesYtd} campaign={campaign} />
        <ImmunityGap data={data.underImmunizedChildren} campaign={campaign} />
      </div>
    );
  },
});

module.exports = Impact;
