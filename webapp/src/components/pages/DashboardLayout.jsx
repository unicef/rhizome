import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import Placeholder from 'components/molecules/Placeholder'
import DashboardHeader from 'components/organisms/DashboardHeader'
import DashboardRow from 'components/organisms/DashboardRow'

import RootStore from 'stores/RootStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'
import DashboardPageStore from 'stores/DashboardPageStore'
import DashboardChartsStore from 'stores/DashboardChartsStore'

import DashboardActions from 'actions/DashboardActions'
import DashboardPageActions from 'actions/DashboardPageActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'

const DashboardLayout = React.createClass({

  mixins: [
    Reflux.connect(DashboardChartsStore, 'charts'),
    Reflux.connect(DashboardPageStore, 'dashboard'),
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
    const header = document.getElementsByClassName('dashboard-header')[0]
    window.addEventListener('scroll', () => this._stickyHeader(header), false)

    // Wait for initial data to be ready and either fetch the dashboard or load a fresh chart
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index && state.campaigns.index) {
        if (this.props.dashboard_id) {
          DashboardPageActions.fetchDashboard(this.props.dashboard_id)
        } else {
          DashboardPageActions.addRow()
          DashboardPageActions.toggleEditMode()
        }
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
    const first_row_charts = nextState.dashboard.rows[0].charts
    const charts = _.toArray(nextState.charts)
    this.missing_params = charts.filter(chart => _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)).length
    this.missing_data = charts.filter(chart => _.isEmpty(chart.data)).length
    this.loading_charts = charts.filter(chart => chart.loading).length
    return !this.missing_data || this.missing_params || this.loading_charts || _.isEmpty(first_row_charts)
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
    const rows = dashboard.rows.map((row, index) => <DashboardRow {...row} editMode={editMode} rowIndex={index}/>)

    let loading = !charts.length > 0 || (!dashboard.rows.length > 0)

    if (!this.props.dashboard_id && dashboard.rows.length > 0) {
      loading = false
    }

    const add_row_button = loading || editMode ? (
      <div className='row text-center'>
        <br/><br/><br/><br/><br/><br/>
        <button
          className='button large'
          onClick={DashboardPageActions.addRow}
          style={{marginTop: '1rem'}}>
          Add Row
        </button>
      </div>
    ) : null

    return (
      <section className='dashboard'>
        <DashboardHeader {...dashboard} dashboard_id={this.props.dashboard_id} selected_locations={selected_locations} />
        { loading ? <Placeholder height={600} /> : rows }
        { add_row_button }
      </section>
    )
  }
})

export default DashboardLayout
