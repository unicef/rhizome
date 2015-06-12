'use strict';

var _      = require('lodash');
var React  = require('react');
var moment = require('moment');

var Impact             = require('dashboard/management/Impact.jsx');
var Performance        = require('dashboard/management/Performance.jsx');
var Access             = require('dashboard/management/Access.jsx');
var BulletChartSection = require('./BulletChartSection.jsx');

var ManagementDashboard = React.createClass({
  propTypes : {
    campaign : React.PropTypes.object,
    region   : React.PropTypes.object,
  },

  getInitialState : function () {
    return {
      data    : [],
      loading : true
    };
  },

  componentWillReceiveProps : function (nextProps) {
    // if (nextProps.campaign.start_date !== this.props.campaign.start_date ||
    //   nextProps.region.id !== this.region.id) {

    //   this._fetch(nextProps.campaign, nextProps.region);
    // }
  },

  render : function () {
    var region   = _.get(this.props, 'region.name', '');
    var campaign = '';

    if (this.props.campaign) {
      campaign = moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('MMM YYYY');
    }

    return (
      <div id='management-dashboard'>
        <div className='row print-only'>
          <div className='small-12 columns'>
            <h1>
              <span className='campaign'>{ campaign }</span>
              <span className='region'>{ region }</span>
            </h1>
            <h2>
              Polio<br />
              Performance<br />
              Dashboard
            </h2>
            <img src='/static/img/UNICEF.svg' className='logo'/>
          </div>
        </div>

        <div className='row'>
          <Impact data={this.state.data} loading={this.state.loading} {...this.props} />
          <Performance data={this.state.data} loading={this.state.loading} {...this.props} />
        </div>

        <div className='row'>
          <section className='medium-2 columns'>
            <h3>FLWs' Capacity to Perform</h3>
            <BulletChartSection data={this.state.data} loading={this.state.loading} cols={2} {...this.props} />
          </section>

          <div className='medium-1 column'>
            <h3>Supply</h3>
            <BulletChartSection data={this.state.data} loading={this.state.loading} cols={1} {...this.props} />
          </div>

          <div className='medium-1 column'>
            <h3>Polio+</h3>
            <BulletChartSection data={this.state.data} loading={this.state.loading} cols={1} {...this.props} />
          </div>

          <div className='medium-1 column'>
            <h3>Resources</h3>
            <BulletChartSection data={this.state.data} loading={this.state.loading} cols={1} {...this.props} />
          </div>

          <Access data={this.state.data} loading={this.state.loading} {...this.props} />
        </div>

      </div>
    );
  },

  _fetch : function (campaign, region) {
    var dt = moment(campaign.end_date, 'YYYY-MM-DD');
    var promises = [];

    // Polio cases
    promises.push(api.datapoints({
      indicator__in  : INDICATORS.cases,
      region__in     : region.id,
      campaign_start : dt.clone().startOf('year').subtract(2, 'years').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in  : INDICATORS.immunityGap,
      region__in     : region.id,
      campaign_start : dt.clone().startOf('quarter').subtract(3, 'years').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in: _(INDICATORS)
        .pick('inaccessibility', 'accessPlans', 'transitPoints', 'microplans', 'totalMissed')
        .values()
        .flatten()
        .value(),
      region__in     : region.id,
      campaign_start : campaign.start,
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in : _(INDICATORS)
        .pick('missed', 'conversions', 'inaccessible')
        .values()
        .flatten()
        .value(),
      region__in     : region.id,
      campaign_start : dt.clone().startOf('month').subtract(1, 'year').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in     : INDICATORS.totalMissed,
      parent_region__in : region.id,
      campaign_start    : campaign.start,
      campaign_end      : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in : _(INDICATORS)
        .pick('capacity', 'polio', 'supply', 'resources')
        .values()
        .flatten()
        .value(),
      region__in     : region.id,
      campaign_start : dt.clone().subtract(4, 'months').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    Promise.all(promises).then(this._loadData);

    this.setState({ loading : true });
  },

  _loadData : function (responses) {
    var data = _(responses)
      .pluck('objects')
      .flatten()
      .map(function (o) {
        // Convert one object with an indicators array into an array of objects
        // each with a single indicator
        var base = _.omit(o, 'indicators');

        return _.map(o.indicators, function (d) {
          return _.assign({}, base, {
            indicator : d.indicator,
            value     : d.value
          });
        });
      })
      .flatten()
      .value();

    this.setState({
      data    : data,
      loading : false
    });
  }
});

module.exports = ManagementDashboard;
