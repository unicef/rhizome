import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import Chart from '02-molecules/Chart'

import ChartStore from 'stores/ChartStore'
import RootStore from 'stores/RootStore'

import ChartActions from 'actions/ChartActions'
import IndicatorActions from 'actions/IndicatorActions'
import CampaignActions from 'actions/CampaignActions'
import LocationActions from 'actions/LocationActions'
import OfficeActions from 'actions/OfficeActions'

import ChartAPI from 'data/requests/ChartAPI'
import CampaignAPI from 'data/requests/CampaignAPI'
import DropdownMenu from '02-molecules/menus/DropdownMenu'
import ExportPdf from '02-molecules/ExportPdf'
import prepChartData from '00-utilities/chart_builder/processChartData'
import ChartFactory from '02-molecules/charts'

var ChartPage = React.createClass({

  mixins: [
    Reflux.connect(RootStore, 'rootStore'),
    Reflux.connect(ChartStore)
  ],

  propTypes: {
    chart_id: React.PropTypes.number
  },

  componentWillMount () {
    ChartActions.fetchChart(this.props.chart_id)
  },

  render () {
    let chart_component = ''
    let chart_title = ''
    let position = {top: 19, right: 0, bottom: 0, left: 0, zIndex: 9997 }
    let message = (<span><i className='fa fa-spinner fa-spin'></i>&nbsp;Loading</span>)

    if (this.state.datapoints && this.state.chartDef) {
      const chart = prepChartData(
        this.state.chartDef,
        this.state.datapoints,
        this.state.selectedLocations,
        this.state.selectedIndicators,
        this.state.rootStore.indicatorIndex
      )

      ChartFactory(this.state.chartDef.type, React.findDOMNode(this), chart.data, chart.options)

      chart_title = this.state.chart.title
      message = <span></span>
    }

    return (
      <div className='row layout-basic'>
        <div className='medium-12 columns text-center'>
          <h1>{ chart_title }</h1>
        </div>
        <div className='medium-2 columns'>
          <a href={'/charts/' + this.props.chart_id + '/edit'} className='button expand small'>
            <i className='fa fa-pencil'></i> Edit Chart
          </a>
          <ExportPdf className='button expand small' />
        </div>
        <div className='medium-10 columns'>
          <div style={position} className='overlay'>
            <div>
              <div>{ message }</div>
            </div>
          </div>
        </div>
      </div>
    )
  }
})

export default ChartPage
