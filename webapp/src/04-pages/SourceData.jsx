import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import page from 'page'
import moment from 'moment'

import randomHash from '00-utilities/randomHash'

import builtins from '03-organisms/dashboard/builtin'
import SourceData from '03-organisms/dashboard/SourceDataDashboard'

import api from 'data/api'
import DashboardAPI from 'data/requests/DashboardAPI'
import DashboardInit from 'data/dashboardInit'

import DashboardStore from 'stores/DashboardStore'
import DataStore from 'stores/DataStore'
import GeoStore from 'stores/GeoStore'
import NavigationStore from 'stores/NavigationStore'

import DashboardActions from 'actions/DashboardActions'
import DataActions from 'actions/DataActions'
import GeoActions from 'actions/GeoActions'

var Dashboard = React.createClass({
  mixins: [
    Reflux.ListenerMixin,
    Reflux.connect(DataStore)
  ],

  getInitialState () {
    return {
      locations: [],
      campaigns: [],
      allCampaigns: [],
      location: null,
      campaign: null,
      dashboard: null,
      allDashboards: []
    }
  },

  getallDashboards () {
    api.get_dashboard().then(res => {
      let customDashboards = _(res.objects).sortBy('id').reverse().value()
      let allDashboards = builtins.concat(customDashboards)
      this.setState({allDashboards: allDashboards})
    })
  },

  componentWillMount () {
    this.getallDashboards()
    page('/datapoints/:dashboard/:location/:year/:month/:doc_tab/:doc_id', this._showSourceData)
    page('/datapoints/:dashboard/:location/:year/:month', this._show)
    page('/datapoints/:dashboard', this._showDefault)
  },

  componentWillUpdate (nextProps, nextState) {
    if (!(nextState.campaign && nextState.location && nextState.dashboard)) {
      return
    }

    let campaign = moment(nextState.campaign.start_date).format('MM/YYYY')
    let title = [
      nextState.dashboard.title,
      [nextState.location.name, campaign].join(' '),
      'RhizomeDB'
    ].join(' - ')

    document.title = title
  },

  componentDidMount () {
    this.listenTo(DashboardStore, this._onDashboardChange)
    this.listenTo(NavigationStore, this._onNavigationChange)
    this.listenTo(DashboardActions.navigate, this._navigate)
    this.listenTo(GeoStore, () => this.forceUpdate())
  },

  _onDashboardChange (state) {
    let fetchData = this.state.loaded

    this.setState(state)

    if (fetchData) {
      let q = DashboardStore.getQueries()
      if (_.isEmpty(q)) {
        DataActions.clear()
      } else {
        if (state.dashboard.builtin) {
          DataActions.fetch(this.state.campaign, this.state.location, q)
        } else {
          DataActions.fetchForDashboard(this.state.dashboard)
        }
      }

      if (this.state.hasMap) { GeoActions.fetch(this.state.location) }
    } else if (NavigationStore.loaded) {
      page({ click: false })
    }
  },

  _onNavigationChange (nav) {
    if (NavigationStore.loaded) {
      page({ click: false })
    }
  },

  _setCampaign (id) {
    let campaign = _.find(this.state.campaigns, c => c.id === id)
    if (!campaign) { return }
    this._navigate({ campaign: moment(campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM') })
  },

  _setLocation (id) {
    let location = _.find(this.state.locations, r => r.id === id)
    if (!location) { return }
    this._navigate({ location: location.name })
  },

  _setDashboard (slug) {
    this._navigate({ dashboard: slug })
  },

  _getDashboard (slug) {
    let dashboard = _.find(this.state.allDashboards, d => _.kebabCase(d.title) === slug)
    if (dashboard.id <= 0) {
      return new Promise(resolve => {
        resolve(dashboard)
      })
    } else {
      return api.get_chart({ dashboard_id: dashboard.id, _: randomHash() }, null, {'cache-control': 'no-cache'}).then(res => {
        let charts = res.objects.map(chart => {
          let result = chart.chart_json
          result.id = chart.id
          return result
        })
        dashboard.charts = _.sortBy(charts, _.property('id'))
        return dashboard
      }, err => {
        console.log(err)
        dashboard.charts = []
      })
    }
  },

  _navigate (params) {
    let slug = _.get(params, 'dashboard', _.kebabCase(this.state.dashboard.title))
    if (params.dashboard) {
      window.location.pathname = '/datapoints/' + slug
    }

    let location = _.get(params, 'location', this.state.location.name)
    let campaign = _.get(params, 'campaign', moment(this.state.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'))
    if (_.isNumber(location)) {
      location = _.find(this.state.locations, r => r.id === location).name
    }
    page('/datapoints/' + [slug, location, campaign].join('/'))
  },

  _showDefault (ctx) {
    api.get_dashboard().then(res => {
      let customDashboards = _(res.objects).sortBy('id').reverse().value()
      let allDashboards = builtins.concat(customDashboards)
      this.setState({ allDashboards: allDashboards })
      this._getDashboard(ctx.params.dashboard).then(dashboard => {
        DashboardActions.setDashboard({
          dashboard
        })
      })
    })
  },

  _show (ctx) {
    NavigationStore.getDashboard(ctx.params.dashboard).then(dashboard => {
      DashboardActions.setDashboard({
        dashboard,
        location: ctx.params.location,
        date: [ctx.params.year, ctx.params.month].join('-')
      })
    })
  },

  _showSourceData (ctx) {
    NavigationStore.getDashboard(ctx.params.dashboard).then(dashboard => {
      let doc_tab = ctx.params.doc_tab

      this.setState({
        doc_id: ctx.params.doc_id,
        doc_tab: doc_tab
      })

      DashboardActions.setDashboard({
        dashboard,
        location: ctx.params.location,
        date: [ctx.params.year, ctx.params.month].join('-')
      })
    })
  },

  render () {
    if (!(this.state.loaded && this.state.dashboard)) {
      let style = {
        fontSize: '2rem',
        zIndex: 9999
      }

      return (
        <div style={style} className='overlay'>
          <div>
            <div><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
          </div>
        </div>
      )
    }

    let {campaign, loading, location, doc_id, doc_tab} = this.state

    let dashboardDef = this.state.dashboard

    let dashboard
    let data = DashboardInit.dashboardInit(
      dashboardDef,
      this.state.data,
      location,
      campaign,
      this.state.locations,
      this.state.allCampaigns,
      GeoStore.features
    )
    let dashboardProps = {
      campaign: campaign,
      dashboard: dashboardDef,
      data: data,
      loading: loading,
      location: location,
      doc_tab: doc_tab,
      doc_id: doc_id
    }
    dashboard = React.createElement(SourceData, dashboardProps)

    let campaigns = _(this.state.campaigns)
      .map(campaign => {
        return _.assign({}, campaign, {
          slug: moment(campaign.start_date).format('MMMM YYYY')
        })
      })
      .sortBy('start_date')
      .reverse()
      .value()

    if (campaign.office_id !== location.office_id) {
      campaign = campaigns[0]
    }

    return (
      <div>
        <div classNameName='clearfix'></div>
        {dashboard}
      </div>
    )
  }
})

export default Dashboard
