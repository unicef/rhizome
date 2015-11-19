'use strict'

import _ from 'lodash'
import React from 'react'
import moment from 'moment'

import Impact from 'dashboard/management/Impact.jsx'
import Performance from 'dashboard/management/Performance.jsx'
import Access from 'dashboard/management/Access.jsx'
import SocialData from 'dashboard/management/SocialData.jsx'
import BulletChartSection from './BulletChartSection.jsx'

var ManagementDashboard = React.createClass({
  propTypes: {
    dashboard: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,

    campaign: React.PropTypes.object,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool,
    location: React.PropTypes.object
  },

  getDefaultProps: function () {
    return {
      data: [],
      loading: true
    }
  },

  render: function () {
    var campaign = this.props.campaign
    var printDate = moment(campaign.start_date).format('MMM ‘YY')
    var data = this.props.data
    var indicators = _.indexBy(this.props.indicators, 'id')
    var loading = this.props.loading
    var location = _.get(this.props, 'location.name', '')
    var dashboardName = 'Management Dashboard'.toUpperCase()
    var pieType = true

    var sections = _(this.props.dashboard.charts)
      .groupBy('section')
      .transform(function (result, charts, sectionName) {
        var section = {}
        _.each(charts, (c, i) => {
          section[_.camelCase(_.get(c, 'title', i))] = _.map(c.indicators, ind => indicators[ind])
        })
        result[sectionName] = section
      })
      .value()

    if (data.__none__.supply.length !== 0) {
      _.filter(data.__none__.supply, d => {
        if (_.isEqual(d.indicator.id, 194)) {
          d.indicator.short_name = 'On-Time OPV Supply'
          if (!_.isNull(d.value)) {
            d.value = 1 - d.value
          }
          _.filter(d.indicator.bound_json, s => {
            var tmpMaxVal = Math.round((1 - s.mn_val) * 1000) / 1000
            s.mn_val = Math.round((1 - s.mx_val) * 1000) / 1000
            s.mx_val = tmpMaxVal
          })
        }
      })
    }

    return (
      <div id='management-dashboard'>
        <div className='row print-only'>
          <div className='medium-4 columns'>
            <h1>
              <span className='location'>{ location }</span>
              <span className='campaign'> { printDate.toUpperCase() }</span>
            </h1>
          </div>
          <div className='medium-2 medium-offset-1 columns'>
            <h2>{dashboardName}</h2>
          </div>
          <div className='medium-1 columns right'>
            <img src='/static/img/RhizomeLogo.png' className='logo' width='100%'/>
          </div>
        </div>

        <div className='row'>
          <Impact data={data.impact} campaign={this.props.campaign} loading={loading} />
          <Performance data={data.performance} campaign={this.props.campaign} loading={loading} location={location}/>
        </div>

        <div className='row'>
          <div className='medium-1 columns'>
            <h3>Soc. Mob.</h3>
            <BulletChartSection data={data.__none__.flwSCapacityToPerform} campaign={campaign} indicators={sections.undefined.flwSCapacityToPerform} loading={loading} cols={1} />
          </div>

          <div className='medium-1 columns'>
            <h3>Vaccinators</h3>
            <BulletChartSection data={data.__none__.vaccinators} campaign={campaign} indicators={sections.undefined.vaccinators} loading={loading} cols={1} />
          </div>

          <div className='medium-1 columns'>
            <h3>Supply</h3>
            <BulletChartSection data={data.__none__.supply} campaign={campaign} indicators={sections.undefined.supply} loading={loading} cols={1} />
          </div>

          <div className='medium-1 columns'>
            <h3>Routine</h3>
            <BulletChartSection data={data.__none__.routine} campaign={campaign} indicators={sections.undefined.routine} loading={loading} cols={1} />
            <h3>Resources</h3>
            <BulletChartSection data={data.__none__.resources} campaign={campaign} indicators={sections.undefined.resources} loading={loading} cols={1} />
          </div>

          <div className='medium-4 columns'>
            <h3>Inaccessible Children</h3>
            <Access data={data.access} campaign={campaign} indicators={indicators} loading={loading} />
            <div className='row'>
              <div className='medium-4 columns right'>
                <h3>Microplan Social Data Usage</h3>
                <SocialData data={data.__none__.microplans} campaign={campaign} loading={loading} pieType={pieType}/>
              </div>
            </div>
          </div>
        </div>

      </div>
    )
  }
})

export default ManagementDashboard
