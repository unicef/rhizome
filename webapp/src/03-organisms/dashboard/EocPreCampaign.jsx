import _ from 'lodash'
import React from 'react'
// import moment from 'moment'
import Chart from '02-molecules/Chart.jsx'
import DashboardActions from 'actions/DashboardActions'

var EocPreCampaign = React.createClass({

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
    // var campaign = this.props.campaign
    // var printDate = moment(campaign.start_date).format('MMM ‘YY')
    var data = this.props.data
    // var indicators = _.indexBy(this.props.indicators, 'id')
    var loading = this.props.loading
    // var location = _.get(this.props, 'location.name', '')
    // var dashboardName = 'EOC Pre Campaig Dashboard'.toUpperCase()

    // var charts = this.props.dashboard.charts

    var tableChart = <Chart type='LineChart'
             data={data.missedChildren}
             loading={loading}
        />

    var mapChart = <Chart type='ChoroplethMap'
             data={data.missedChildrenByProvince}
             loading={loading}
             options={{
               aspect: 0.6,
               domain: _.constant([0, 0.1]),
               value: _.property('properties[475]'),
              //  bubbleValue: _.property('properties[177]'),
              //  stripeValue: _.property('properties[203]'),
              //  xFormat: d3.format(',.1%'),
               onClick: d => { DashboardActions.navigate({ location: d }) }
             }}/>

    var trendChart = <Chart type='LineChart'
             data={data.polioCasesYtd}
             loading={loading}
        />

    return (
    <div id='eoc-dashboard-dashboard'>
      <div className='row'>
        <div className='medium-8 columns end cd-chart-size'>
          <h2>Table Chart</h2>
          {tableChart}
        </div>
        <div className="medium-4 columns end">
          <div className='row'>
            <div className='medium-12 columns end cd-chart-size'>
              <h2>Map Chart</h2>
              {mapChart}
            </div>
          </div>
          <div className='row'>
            <div className='medium-12 columns end cd-chart-size'>
              <h2>Trend Chart</h2>
              {trendChart}
            </div>
          </div>
        </div>
      </div>
    </div>
    )

    // return (<div id='management-dashboard'>
    //   <div className='row print-only'>
    //     <div className='medium-4 columns'>
    //       <h1>
    //         <span className='location'>{ location }</span>
    //         <span className='campaign'> { printDate.toUpperCase() }</span>
    //       </h1>
    //     </div>
    //     <div className='medium-2 medium-offset-1 columns'>
    //       <h2>{dashboardName}</h2>
    //     </div>
    //     <div className='medium-1 columns right'>
    //       <img src='/static/img/RhizomeLogo.png' className='logo' width='100%'/>
    //     </div>
    //   </div>
    //
    //   <div className='row'>
    //     <Impact data={data.impact} campaign={this.props.campaign} loading={loading} />
    //     <Performance data={data.performance} campaign={this.props.campaign} loading={loading} location={location}/>
    //   </div>
    //
    //   <div className='row'>
    //     <div className='medium-1 columns'>
    //       <h3>Soc. Mob.</h3>
    //       <BulletChartSection data={data.__none__.flwSCapacityToPerform} campaign={campaign} indicators={sections.undefined.flwSCapacityToPerform} loading={loading} cols={1} />
    //     </div>
    //
    //     <div className='medium-1 columns'>
    //       <h3>Vaccinators</h3>
    //       <BulletChartSection data={data.__none__.vaccinators} campaign={campaign} indicators={sections.undefined.vaccinators} loading={loading} cols={1} />
    //     </div>
    //
    //     <div className='medium-1 columns'>
    //       <h3>Supply</h3>
    //       <BulletChartSection data={data.__none__.supply} campaign={campaign} indicators={sections.undefined.supply} loading={loading} cols={1} />
    //     </div>
    //
    //     <div className='medium-1 columns'>
    //       <h3>Routine</h3>
    //       <BulletChartSection data={data.__none__.routine} campaign={campaign} indicators={sections.undefined.routine} loading={loading} cols={1} />
    //       <h3>Resources</h3>
    //       <BulletChartSection data={data.__none__.resources} campaign={campaign} indicators={sections.undefined.resources} loading={loading} cols={1} />
    //     </div>
    //
    //     <div className='medium-4 columns'>
    //       <h3>Inaccessible Children</h3>
    //       <Access data={data.access} campaign={campaign} indicators={indicators} loading={loading} />
    //       <div className='row'>
    //         <div className='medium-4 columns right'>
    //           <h3>Microplan Social Data Usage</h3>
    //           <SocialData data={data.__none__.microplans} campaign={campaign} loading={loading}/>
    //         </div>
    //       </div>
    //     </div>
    //   </div>
    // </div>)
  }
})

export default EocPreCampaign
