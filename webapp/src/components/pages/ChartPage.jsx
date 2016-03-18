import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import Chart from 'components/molecules/Chart'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import ExportPdf from 'components/molecules/ExportPdf'
import ChartFactory from 'components/molecules/charts_d3/ChartFactory'
import ChartInfo from 'components/molecules/charts_d3/ChartInfo'

import ChartStore from 'stores/ChartStore'
import LocationStore from 'stores/LocationStore'
import CampaignStore from 'stores/CampaignStore'
import IndicatorStore from 'stores/IndicatorStore'
import DatapointStore from 'stores/DatapointStore'

import ChartActions from 'actions/ChartActions'
import IndicatorActions from 'actions/IndicatorActions'
import CampaignActions from 'actions/CampaignActions'
import LocationActions from 'actions/LocationActions'
import OfficeActions from 'actions/OfficeActions'

import ChartAPI from 'data/requests/ChartAPI'
import CampaignAPI from 'data/requests/CampaignAPI'

var ChartPage = React.createClass({

  mixins: [
    Reflux.connect(ChartStore, 'chart'),
  ],

  propTypes: {
    chart_id: React.PropTypes.number
  },

  componentWillMount () {
    ChartActions.fetchChart(this.props.chart_id)
  },

  render () {
    const chart = this.state.chart
    return (
      <div className='row layout-basic'>
        <div className='medium-12 columns text-center'>
          <h1>{ chart.def.title }</h1>
        </div>
        <div className='medium-2 columns'>
          <a href={'/charts/' + this.props.chart_id + '/edit'} className='button expand small'>
            <i className='fa fa-pencil'></i> Edit Chart
          </a>
          <ExportPdf className='button expand small' />
        </div>
        <div className='medium-10 columns'>
          <Chart type={chart.def.type} data={chart.data} options={chart.def} />
        </div>
      </div>
    )
  }
})

export default ChartPage
