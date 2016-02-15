import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import Chart from '02-molecules/Chart'

import DataStore from 'stores/DataStore'
import DataActions from 'actions/DataActions'

import ChartAPI from 'data/requests/ChartAPI'

var ChartPage = React.createClass({

  mixins: [
    Reflux.connect(DataStore)
  ],

  propTypes: {
      chart_id: React.PropTypes.number
  },

  getInitialState () {
    return {
      chart: null
    }
  },

  componentWillMount () {
    ChartAPI.getChart(this.props.chart_id).then(response => {
      let chartDef = JSON.parse(response.chart_json)
      this.setState({
        chart: chartDef,
        data: DataActions.fetchForChart(chartDef)
      })
    })
  },

  render () {
    if (this.state.data.data) {
      return (
        <div>
          <a href={'/datapoints/charts/' + this.props.chart_id + '/edit'} className='button'>
            <i className='fa fa-pencil'></i>
            Edit Chart
          </a>
          <Chart id='custom-chart' type={this.state.chart.type} data={this.state.data.data}
        options={this.state.data.options}/>
        </div>
      )
    } else {
      return <h1>Chart View Coming Soon</h1>
    }
  }
})

export default ChartPage
