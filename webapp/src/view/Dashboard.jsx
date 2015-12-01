import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import page from 'page'
import moment from 'moment'

import api from 'data/api'
import DashboardInit from 'data/dashboardInit'
import builtins from 'dashboard/builtin'
import randomHash from 'util/randomHash'

import TitleMenu from 'component/TitleMenu.jsx'
import RegionTitleMenu from 'component/RegionTitleMenu'
import CampaignTitleMenu from 'component/CampaignTitleMenu.jsx'
import MenuItem from 'component/MenuItem.jsx'

import CustomDashboard from 'dashboard/CustomDashboard.jsx'

import DashboardStore from 'stores/DashboardStore'
import DataStore from 'stores/DataStore'
import GeoStore from 'stores/GeoStore'
import IndicatorStore from 'stores/IndicatorStore'
import NavigationStore from 'stores/NavigationStore'

import DashboardActions from 'actions/DashboardActions'
import DataActions from 'actions/DataActions'
import GeoActions from 'actions/GeoActions'

const LAYOUT = {
  'Management Dashboard': require('dashboard/ManagementDashboard.jsx'),
  'NGA Campaign Monitoring': require('dashboard/NCODashboard.jsx'),
  'District Dashboard': require('dashboard/District.jsx'),
  'Source Data': require('dashboard/SourceDataDashboard.jsx')
}

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
      let customDashboards = _(res.objects).sortBy('title').value()
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

    this.listenTo(IndicatorStore, () => this.forceUpdate())
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
          DataActions.fetchForChart(this.state.dashboard)
        }
      }

      if (this.state.hasMap) {
        GeoActions.fetch(this.state.location)
      }
    } else if (NavigationStore.loaded) {
      page({
        click: false
      })
    }
  },

  _onNavigationChange (nav) {
    if (NavigationStore.loaded) {
      page({
        click: false
      })
    }
  },

  _setCampaign (id) {
    let campaign = _.find(this.state.campaigns, c => c.id === id)

    if (!campaign) {
      return
    }

    this._navigate({
      campaign: moment(campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM')
    })
  },

  _setLocation (id) {
    let location = _.find(this.state.locations, r => r.id === id)

    if (!location) {
      return
    }

    this._navigate({
      location: location.name
    })
  },

  _setDashboard (slug) {
    this._navigate({
      dashboard: slug
    })
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
      let customDashboards = _(res.objects).sortBy('title').value()
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
    let dashboardName = _.get(dashboardDef, 'title', '')

    let indicators = IndicatorStore.getById.apply(
      IndicatorStore,
      _(_.get(dashboardDef, 'charts', []))
        .pluck('indicators')
        .flatten()
        .uniq()
        .value()
    )

    let dashboard
    if (Object.keys(LAYOUT).indexOf(dashboardName) >= 0) {
      let data = DashboardInit.dashboardInit(
        dashboardDef,
        this.state.data,
        location,
        campaign,
        this.state.locations,
        this.state.allCampaigns,
        indicators,
        GeoStore.features
      )
      let dashboardProps = {
        campaign: campaign,
        dashboard: dashboardDef,
        data: data,
        indicators: indicators,
        loading: loading,
        location: location,
        doc_tab: doc_tab,
        doc_id: doc_id
      }
      dashboard = React.createElement(LAYOUT[dashboardName], dashboardProps)
    } else {
      let customDashboardProps = {
        campaigns: this.state.allCampaigns,
        dashboard: dashboardDef,
        data: Array.isArray(this.state.data) ? {} : this.state.data,
        indicators: indicators,
        loading: loading
      }
      dashboard = React.createElement(CustomDashboard, customDashboardProps)
    }

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

    let dashboardItems = MenuItem.fromArray(
      _.map(this.state.allDashboards, d => {
        return {
          title: d.title,
          value: _.kebabCase(d.title)
        }
      }),
      this._setDashboard)

    let edit
    if (dashboardDef.owned_by_current_user) {
      edit = (
        <span>
          <a className='menu-button fa-stack'
             href={'/datapoints/dashboards/edit/' + dashboardDef.id + '/'}>
            <i className='fa fa-stack-2x fa-circle'></i>
            <i className='fa fa-stack-1x fa-pencil'></i>
          </a>
          &emsp;
        </span>
      )
    }

    let settingFilter = ''
    if (dashboardDef.builtin === true) {
      settingFilter = (<div className='row'>
        <div className='medium-6 columns'>
          <RegionTitleMenu
            locations={this.state.locations}
            selected={location}
            sendValue={this._setLocation}/>
        </div>
        <div className='medium-6 columns'>
          <CampaignTitleMenu
            campaigns={campaigns}
            selected={campaign}
            sendValue={this._setCampaign}/>
        </div>
      </div>)
    }

    return (
      <div>
        <div classNameName='clearfix'></div>
        <form className='inline no-print cd-titlebar'>
          <div className='row'>
            <div className='medium-6 columns'>
              {settingFilter}
            </div>
            <div className='medium-3 columns'>
              <div>
                {edit}
                <TitleMenu text={dashboardName}
                           icon='fa-chevron-down'
                           className='cd-titlebar-margin'>
                  {dashboardItems}
                </TitleMenu>
              </div>
            </div>
          </div>
        </form>
        {dashboard}
      </div>
    )
  }
})

export default Dashboard
