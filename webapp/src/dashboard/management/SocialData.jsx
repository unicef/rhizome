'use strict';

var _      = require('lodash');
var React  = require('react');

var PieChartList = require('component/PieChartList.jsx');
var Chart = require('component/Chart.jsx');

var colors = require('colors');

var indicatorForCampaign = function (campaign, indicator) {
  return d => d.campaign.id === campaign && d.indicator.id === indicator;
};

var SocialData = React.createClass({
  propTypes : {
    campaign: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,
    data: React.PropTypes.object,
  },

  render : function() {
    var data     = this.props.data;
    var campaign = this.props.campaign;
    var loading  = this.props.loading;

    var social = _.find(data, indicatorForCampaign(campaign.id, 28));
    var microplans = _.find(data, indicatorForCampaign(campaign.id, 27));

    var microplansText = function () {
      var num = _.get(social, '[0][0].value');
      var den = _.get(microplans, 'value');

      return _.isFinite(num) && _.isFinite(den) ?
      num + ' / ' + den + ' microplans incorporate social data' :
        '';
    };

    social = !_.isEmpty(social) ? [[social]] : [];

    return (
        <div className="row">
          <div className="medium-4 columns">
              <PieChartList
              loading={loading}
              keyPrefix='microplans'
              data={social}
              name={microplansText}
              emptyText='No microplan data available'
              options={{
                domain  : _.constant([0, _.get(microplans, 'value', 1)]),
                size    : 24,
                palette : colors
              }}/>
          </div>
        </div>
    );
  }
});

module.exports = SocialData;
