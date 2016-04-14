import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import AsyncButton from 'components/atoms/AsyncButton'

import Placeholder from 'components/molecules/Placeholder'
import MultiChart from 'components/organisms/MultiChart'
import DashboardRow from 'components/organisms/DashboardRow'
import TitleInput from 'components/molecules/TitleInput'

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

  getInitialState: function () {
    return {
      titleEditMode: false
    }
  },

  componentDidMount: function () {
    // Wait for initial data to be ready and either fetch the dashboard or load a fresh chart
    RootStore.listen(() => {
      const state = this.state
      if (state.locations.index && state.indicators.index && state.campaigns.index) {
        if (this.props.dashboard_id) {
          DashboardPageActions.fetchDashboard(this.props.dashboard_id)
        } else {
          DashboardPageActions.addRow()
          DashboardPageActions.toggleEditMode()
          DashboardChartsActions.addChart()
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
    const charts = _.toArray(nextState.charts)
    this.missing_params = charts.filter(chart => _.isEmpty(chart.selected_indicators) || _.isEmpty(chart.selected_locations)).length
    this.missing_data = charts.filter(chart => _.isEmpty(chart.data)).length
    this.loading_charts = charts.filter(chart => chart.loading).length
    return !this.missing_data || this.missing_params || this.loading_charts
  },

  _toggleTitleEdit: function (title) {
    if (_.isString(title)) {
      DashboardPageActions.setDashboardTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  renderChartSpace: function (index) {
    return (
      <article className='multi-chart medium-12 columns'>
        <header className='row'>
          <div className='medium-12 columns chart-header text-center'><h2>Chart</h2></div>
        </header>
        <section className='row'>
          <div class='text-center' style={{width: '100%'}}>
            <br/><br/>
            <button className='button large' onClick={DashboardChartsActions.addChart} style={{marginTop: '1rem'}}>
              Add Chart
            </button>
            <br/><br/>
          </div>
        </section>
      </article>
    )
  },

  render: function () {
    const editMode = this.state.dashboard.editMode
    const dashboard = this.state.dashboard
    const chart_uuids = this.state.dashboard.chart_uuids
    const charts = _.toArray(this.state.charts)
    const title_bar = this.state.titleEditMode ?
      <TitleInput initialText={dashboard.title} save={this._toggleTitleEdit}/>
      :
      <h1 onClick={this._toggleTitleEdit}>
        <a>{dashboard.title || 'Untitled Dashboard'}</a>
      </h1>

    const chart_components = chart_uuids.map(uuid => {
      const chart = this.state.charts[uuid]
      return (
        <MultiChart
          chart={chart}
          readOnlyMode={!editMode}
          linkCampaigns={() => DashboardChartsActions.toggleCampaignLink(chart.uuid)}
          duplicateChart={DashboardChartsActions.duplicateChart}
          selectChart={new_chart => DashboardChartsActions.selectChart(new_chart, chart.uuid)}
          toggleSelectTypeMode={() => DashboardChartsActions.toggleSelectTypeMode(chart.uuid)}
          toggleEditMode={() => DashboardChartsActions.toggleChartEditMode(chart.uuid)}
          removeChart={DashboardChartsActions.removeChart}
          saveChart={() => DashboardChartsActions.saveChart(chart.uuid)}
          setDateRange={(key, value) => DashboardChartsActions.setDateRange(key, value, chart.uuid)}
          setGroupBy={(grouping) => DashboardChartsActions.setGroupBy(grouping, chart.uuid)}
          setPalette={(palette) => DashboardChartsActions.setPalette(palette, chart.uuid)}
          setTitle={(title) => DashboardChartsActions.setChartTitle(title, chart.uuid)}
          setType={(type) => DashboardChartsActions.setType(type, chart.uuid)}
          setIndicators={(indicators) => DashboardChartsActions.setIndicators(indicators, chart.uuid)}
          selectIndicator={(id) => DashboardChartsActions.selectIndicator(id, chart.uuid)}
          deselectIndicator={(id) => DashboardChartsActions.deselectIndicator(id, chart.uuid)}
          reorderIndicator={(indicators) => DashboardChartsActions.reorderIndicator(indicators, chart.uuid)}
          clearSelectedIndicators={() => DashboardChartsActions.clearSelectedIndicators(chart.uuid)}
          setLocations={(locations) => DashboardChartsActions.setLocations(locations, chart.uuid)}
          selectLocation={(id) => DashboardChartsActions.selectLocation(id, chart.uuid)}
          deselectLocation={(id) => DashboardChartsActions.deselectLocation(id, chart.uuid)}
          clearSelectedLocations={() => DashboardChartsActions.clearSelectedLocations(chart.uuid)}
          setCampaigns={(campaigns) => DashboardChartsActions.setCampaigns(campaigns, chart.uuid)}
          selectCampaign={(id) => DashboardChartsActions.selectCampaign(id, chart.uuid)}
          deselectCampaign={(id) => DashboardChartsActions.deselectCampaign(id, chart.uuid)}
        />
      )
    })

    const rows = dashboard.rows.map(row => <DashboardRow {...row} />)

    const add_chart_button = loading || editMode ? (
      <div className='row text-center'>
        <button
          className='button large'
          onClick={DashboardChartsActions.addChart}
          style={{marginTop: '1rem'}}>
          Add Chart
        </button>
      </div>
    ) : null

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

    const save_dashboard_button = editMode ? (
      <AsyncButton
        text='Save Dashboard'
        alt_text='Saving ...'
        isBusy={dashboard.saving}
        onClick={() => DashboardPageActions.saveDashboard(this.props.dashboard_id)}
      />
    ) : null

    const loading = !charts.length > 0

    return (
      <section className='dashboard'>
        <header className='row dashboard-header'>
          <div className='medium-6 columns medium-text-left small-text-center'>
            { editMode ? title_bar : <h1>{dashboard.title || 'Untitled Dashboard'}</h1> }
          </div>
          <div className='medium-6 columns medium-text-right small-text-center'>
            { save_dashboard_button }
            <button className='button' onClick={DashboardPageActions.toggleEditMode}>
              { !editMode ? 'Edit Dashboard' : 'Exit Edit Mode' }
            </button>
          </div>
        </header>
        { loading ? <Placeholder height={600} /> : rows}
        { add_row_button }
      </section>
    )
  }
})

export default DashboardLayout
