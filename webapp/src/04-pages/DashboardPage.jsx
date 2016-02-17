import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import page from 'page'
import moment from 'moment'

import randomHash from '00-utilities/randomHash'

import RegionTitleMenu from '02-molecules/menus/RegionTitleMenu'
import CampaignTitleMenu from '02-molecules/menus/CampaignTitleMenu'
import ExportPdf from '02-molecules/ExportPdf'

import builtins from '03-organisms/dashboard/builtin'
import CustomDashboard from '03-organisms/dashboard/CustomDashboard'

import Indicator from 'data/requests/IndicatorAPI'
import api from 'data/api'
import DashboardInit from 'data/dashboardInit'

import DashboardStore from 'stores/DashboardStore'
import DataStore from 'stores/DataStore'
import GeoStore from 'stores/GeoStore'
import NavigationStore from 'stores/NavigationStore'

import DashboardActions from 'actions/DashboardActions'
import DataActions from 'actions/DataActions'
import GeoActions from 'actions/GeoActions'

const LAYOUT = {
  'Management Dashboard': require('03-organisms/dashboard/ManagementDashboard'),
  'NGA Campaign Monitoring': require('03-organisms/dashboard/NCODashboard'),
  'District Dashboard': require('03-organisms/dashboard/District'),
  'Source Data': require('03-organisms/dashboard/SourceDataDashboard')
}

var DashboardPage = React.createClass({
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

  editChart (index) {
    this.setState({chartBuilderindex: index, chartBuilderActive: true})
  },

  getAllDashboards () {
    api.get_dashboard().then(res => {
      let customDashboards = _(res.objects).sortBy('id').reverse().value()
      let allDashboards = builtins.concat(customDashboards)
      this.setState({allDashboards: allDashboards})
    })
  },

  componentWillMount () {
    // this.getAllDashboards()
    page('/datapoints/dashboards/:dashboard/:location/:year/:month/:doc_tab/:doc_id', this._showSourceData)
    page('/datapoints/dashboards/:dashboard/:location/:year/:month', this._show)
    page('/datapoints/dashboards/:dashboard', this._showDefault)
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

    Indicator.getIndicators().then(indicators => {
      this.indicators = indicators
      this.forceUpdate()
    })
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

  _setDashboard (id) {
    this._navigate({
      dashboard: id
    })
  },

  _getDashboard (slug) {
    let dashboard = _.find(this.state.allDashboards, d => _.kebabCase(d.title) === slug)

    if (/^\d+$/.test(slug)) {
      dashboard = _.find(this.state.allDashboards, d => _.kebabCase(d.id) === slug)
    }

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
      window.location.pathname = '/datapoints/dashboards/' + slug
    }

    let location = _.get(params, 'location', this.state.location.name)
    if (_.isNumber(location)) {
      location = _.find(this.state.locations, r => r.id === location).name
    }

    let campaign_dates = _.get(params, 'campaign', moment(this.state.campaigns[0].start_date, 'YYYY-MM-DD').format('YYYY/MM'))
    if (typeof this.state.campaign !== 'undefined') {
      campaign_dates = _.get(params, 'campaign', moment(this.state.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'))
    }

    page('/datapoints/dashboards/' + [slug, location, campaign_dates].join('/'))
  },

  _showDefault (ctx) {
    this.setState({ allDashboards: NavigationStore.dashboards })
    this._getDashboard(ctx.params.dashboard).then(dashboard => {
      DashboardActions.setDashboard({dashboard})
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
    if (!(this.state.dashboard)) {
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

    let campaigns = _(this.state.campaigns)

    let campaignExists = typeof campaign !== 'undefined'
    if (!campaignExists || (campaign.office_id !== location.office_id)) {
      campaign = campaigns.first()
    };

    let indicators
    if (this.indicators) {
      indicators = _(_.get(dashboardDef, 'charts', []))
        .pluck('indicators')
        .flatten()
        .uniq()
        .map(id => this.indicators[id])
        .value()
    }

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
        loading: loading
      }
      dashboard = React.createElement(CustomDashboard, customDashboardProps)
    }

    campaigns = campaigns.map(campaign => {
      return _.assign({}, campaign, {
        slug: moment(campaign.start_date).format('MMMM YYYY')
      })
    })
    .sortBy('start_date')
    .reverse()
    .value()

    // if (dashboardDef.owned_by_current_user) {
    // this should be an onClick -- not a link.  see DashboardBuilder.jsx -- this.editChart
    let edit = (
        <span style={{'display': 'inline', 'textAlign': 'right'}}>
          <a className='menu-button fa-stack'
             href={'/datapoints/dashboards/' + dashboardDef.id + '/edit/'}>
            <i className='fa fa-stack-1x fa-pencil' style={{ display: 'inline-block' }}></i>
          </a>
        </span>
      )

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
            location={location}
            sendValue={this._setCampaign}/>
        </div>
      </div>)
    }
    let exportModule = (<ExportPdf className='export-file' />)

    return (
      <div>
        <div classNameName='clearfix'></div>
        <form className='inline no-print cd-titlebar'>
          <div className='row'>
            <div className='medium-6 columns'>
              {settingFilter}
            </div>
            <div className={dashboardDef.builtin === true ? 'medium-3 columns' : 'medium-3 columns medium-offset-6'}>
              <div className='row'>
                <div className='medium-5 columns medium-offset-5'>
                  {exportModule}
                </div>
                <div>
                  {edit}
                </div>
              </div>
            </div>
          </div>
        </form>
        {dashboard}
      </div>
    )
  }
})

export default DashboardPage
