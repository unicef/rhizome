import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import StateMixin from 'reflux-state-mixin'

import Chart from 'components/molecules/Chart'
import ExportPdf from 'components/molecules/ExportPdf'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'

import ChartActions from 'actions/ChartActions'

import RootStore from 'stores/RootStore'
import DashboardPageStore from 'stores/DashboardPageStore'

var DashboardPage = React.createClass({

  mixins: [
    StateMixin.connect(RootStore, 'rootStore'),
    // StateMixin.connect(DashboardPageStore),
  ],

   propTypes: {
    campaign: React.PropTypes.object,
    charts_ids: React.PropTypes.array
  },

  getDefaultProps () {
    return {
      chart_ids: [5, 3],
    }
  },

  charts: [],

  componentDidMount () {

  },

  render () {
    return (
      <div className='row layout-basic'>
        <h1>we need a chart</h1>
      </div>
    )
  }
})

export default DashboardPage
