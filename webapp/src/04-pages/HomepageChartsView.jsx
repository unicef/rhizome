import React from 'react'
import Reflux from 'reflux'

import HomepageChartsSection from '03-organisms/HomepageChartsSection'

import HomepageDashboardsStore from 'stores/HomepageDashboardsStore'
import HomepageDashboardsActions from 'actions/HomepageDashboardsActions'

var HomepageChartsView = React.createClass({
  mixins: [
    Reflux.ListenerMixin,
    Reflux.connect(HomepageDashboardsStore, 'dashboards')
  ],

  getInitialState: function () {
    return {
      dashboards: []
    }
  },

  componentWillMount () {
    HomepageDashboardsActions.initialize()
  },

  render: function () {
    if (this.state.dashboards.length === 0) {
      return (
        <div>
          <div className='large-4 columns chart-container'>
            <div className='chart--placeholder'>
              <div className='chart--placeholder__loading'><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
            </div>
          </div>
          <div className='large-4 columns chart-container'>
            <div className='chart--placeholder'>
              <div className='chart--placeholder__loading'><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
            </div>
          </div>
          <div className='large-4 columns chart-container'>
            <div className='chart--placeholder'>
              <div className='chart--placeholder__loading'><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
            </div>
          </div>
        </div>)
    }
    var list = []
    this.state.dashboards.dashboards.forEach(function (item) {
      var dashboardProps = {
        campaign: item.campaign,
        data: item.data,
        indicators: item.indicators,
        location: item.location,
        mapLoading: item.mapLoading
      }
      list.push(<HomepageChartsSection location={item.location.name} data={dashboardProps}/>)
    })

    return (
      <div>
        {list}
      </div>
    )
  }
})

export default HomepageChartsView
