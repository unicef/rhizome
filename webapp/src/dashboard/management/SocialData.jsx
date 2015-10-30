'use strict';

var _      = require('lodash');
var React  = require('react');

var BulletChartSection = require('dashboard/BulletChartSection.jsx');

var SocialData = React.createClass({
  propTypes : {
    campaign: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
  },

  render : function() {
    var data     = this.props.data;
    var campaign = this.props.campaign;
    var indicators = this.props.indicators;
    var loading  = this.props.loading;

    return (
        <div className="row">
          <div className="medium-4 columns">
            <BulletChartSection data={data} campaign={campaign} indicators={indicators} loading={loading} cols={1} />
          </div>
        </div>
    );
  }
});

module.exports = SocialData;