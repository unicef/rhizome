import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import Chart from '02-molecules/Chart'

import DataStore from 'stores/DataStore'
import DataActions from 'actions/DataActions'

import ChartAPI from 'data/requests/ChartAPI'
import CampaignAPI from 'data/requests/CampaignAPI'
import DropdownMenu from '02-molecules/menus/DropdownMenu'

var ChartPage = React.createClass({

  mixins: [
    Reflux.connect(DataStore)
  ],

  propTypes: {
      chart_id: React.PropTypes.number
  },

  componentWillMount () {
    CampaignAPI.getCampaigns().then(response => {
      this.setState({ campaigns: response })
    })
    ChartAPI.getChart(this.props.chart_id).then(response => {
      let chartDef = response.chart_json
      this.setState({
        chart: chartDef,
        data: DataActions.fetchForChart(chartDef)
      })
    })
  },

  render () {
    if (this.state.data.data) {
      return (
        <div className='row layout-basic'>
          <div className='medium-12 columns text-center'>
            <h1>{ this.state.chart.title }</h1>
          </div>
          <div className='medium-2 columns'>
            <a href={'/datapoints/charts/' + this.props.chart_id + '/edit'} className='button expand small'>
              <i className='fa fa-pencil'></i>
               Edit Chart
            </a>
          </div>
          <div className='medium-10 columns'>
            <Chart id='custom-chart' type={this.state.chart.type} data={this.state.data.data}
          options={this.state.data.options} campaigns={this.state.campaigns} defaultCampaign={this.state.campaigns[0]}/>
          </div>
        </div>
      )
    } else {
      return  (
        <div className='loading'>
          <i className='fa fa-spinner fa-spin fa-5x'></i>
          <div>Loading</div>
        </div>
      )
    }
  }
})

export default ChartPage
