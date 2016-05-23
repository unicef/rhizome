import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import Placeholder from 'components/Placeholder'
import DashboardHeader from 'components/organisms/dashboard/DashboardHeader'
import DashboardRow from 'components/organisms/dashboard/DashboardRow'

import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import DashboardContainerStore from 'stores/DashboardContainerStore'
import DashboardChartsStore from 'stores/DashboardChartsStore'

import RootActions from 'actions/RootActions'
import DashboardActions from 'actions/DashboardActions'
import DashboardContainerActions from 'actions/DashboardContainerActions'

const DashboardContainer = React.createClass({

  mixins: [
    Reflux.connect(DashboardChartsStore, 'charts'),
    Reflux.connect(DashboardContainerStore, 'dashboard'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    dashboard_id: PropTypes.number
  },

  getDefaultProps: function () {
    return {
      dashboard_id: null
    }
  },

  componentDidMount: function () {
    document.getElementsByTagName('body')[0].className += ' dashboard-page'
    const header = document.getElementsByClassName('page-header')[0]
    window.addEventListener('scroll', () => this._stickyHeader(header), false)

    // Wait for initial data to be ready and either fetch the dashboard or load a fresh chart
    this.listenTo(RootActions.fetchAllMeta.completed, (response) => {
      if (this.props.dashboard_id) {
        DashboardContainerActions.fetchDashboard(this.props.dashboard_id)
      } else {
        DashboardContainerActions.addRow()
        DashboardContainerActions.toggleEditMode()
      }
    })
    // If the dashboard is saved for the first time, redirect to the dashboard page
    this.listenTo(DashboardActions.postDashboard.completed, (response) => {
      if (!this.props.dashboard_id) {
        const dashboard_id = response.objects.id
        window.location = window.location.origin + '/dashboards/' + dashboard_id
      }
    })
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    const first_row_charts = !nextProps.dashboard_id ? nextState.dashboard.rows[0].charts : []
    const charts = _.toArray(nextState.charts)
    this.missing_params = charts.filter(chart => _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)).length
    this.missing_data = charts.filter(chart => _.isEmpty(chart.data)).length
    this.loading_charts = charts.filter(chart => chart.loading).length
    return !this.missing_data || this.missing_params || this.loading_charts || _.isNull(first_row_charts)
  },

  _stickyHeader: function (header) {
    if (window.pageYOffset > 93) {
      header.classList.add('fixed')
    }
    if (window.pageYOffset < 92) {
      header.classList.remove('fixed')
    }
  },

  render: function () {
    const editMode = this.state.dashboard.editMode
    const dashboard = this.state.dashboard
    const charts = _.toArray(this.state.charts)
    const selected_locations = charts[0] ? charts[0].selected_locations : []
    const selected_campaigns = charts[0] ? charts[0].selected_campaigns : []
    const indicator_filter = charts[0] ? charts[0].indicator_filter : []
    const rows = noRows ? [] : dashboard.rows.map((row, index) => {
      return (
        <DashboardRow
          all_charts={this.state.charts}
          editMode={editMode}
          rowIndex={index}
          totalRows={dashboard.rows.length}
          {...row}
        />
      )
    })
    const noRows = dashboard.rows.length <= 0
    const noCharts = charts.length <= 0

    let loading = noCharts || noRows

    if (!this.props.dashboard_id && !noRows) {
      loading = false
    }

    const add_row_button = loading || editMode ? (
      <div className='row text-center'>
        <br/><br/><br/><br/><br/><br/>
        <button
          className='button large'
          onClick={DashboardContainerActions.addRow}
          style={{marginTop: '1rem'}}>
          Add Row
        </button>
      </div>
    ) : null

    return (
      <section className='dashboard'>
        <DashboardHeader {...dashboard}
          dashboard_id={this.props.dashboard_id}
          selected_campaigns={selected_campaigns}
          selected_locations={selected_locations}
          indicator_filter={indicator_filter}
        />
        { loading ? <Placeholder height={600} /> : rows }
        { add_row_button }
      </section>
    )
  }
})

export default DashboardContainer
