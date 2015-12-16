import React from 'react'
import Reflux from 'reflux'

import PdfChartBlock from 'view/pdf-test/PdfChartBlock.jsx'
import HomepageDashboardsStore from 'stores/HomepageDashboardsStore'

import HomepageDashboardsActions from 'actions/HomepageDashboardsActions'

var PdfChartTestView = React.createClass({
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
          <div className='pdf-chart columns chart-container'>
            <div className='chart--placeholder'>
              <div className='chart--placeholder__loading'><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
            </div>
          </div>
        </div>)

      /*
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
      */
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

      list.push(<PdfChartBlock location={item.location} data={dashboardProps}/>)
    })

    var item = list[0]

    return (
      <div>
        {item}
      </div>
    )
  }
})

export default PdfChartTestView
