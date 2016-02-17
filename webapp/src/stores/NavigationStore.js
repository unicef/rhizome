import _ from 'lodash'
import Reflux from 'reflux'
import moment from 'moment'

import CampaignStore from 'stores/CampaignStore'
import Office from 'data/requests/OfficeAPI'

import api from 'data/api'
import builtins from '03-organisms/dashboard/builtin'
import randomHash from '00-utilities/randomHash'

var NavigationStore = Reflux.createStore({
  init: function () {
    this.campaigns = []
    this.dashboards = []
    this.customDashboards = []
    this.customCharts = []
    this.loaded = false

    Promise.all([
      CampaignStore.getCampaignsPromise(),
      api.get_dashboard(),
      Office.getOffices()
    ]).then(_.spread(this._loadDashboards))
  },

  getInitialState: function () {
    return {
      campaigns: this.campaigns,
      dashboards: this.dashboards,
      customCharts: this.customCharts,
      documents: this.documents,
      loaded: this.loaded
    }
  },

  // API
  getDashboard: function (slug) {
    var dashboard = _.find(this.dashboards, d => _.kebabCase(d.title) === slug)

    if (dashboard.id <= 0) {
      return new Promise(resolve => {
        resolve(dashboard)
      })
    } else {
      return api.get_chart({ dashboard_id: dashboard.id, _: randomHash() }, null, {'cache-control': 'no-cache'}).then(res => {
        let charts = res.objects.map(chart => {
          var result = chart.chart_json
          result.id = chart.id
          return result
        })
        dashboard.charts = _.sortBy(charts, _.property('id'))
        return dashboard
      }, function (err) {
        console.log(err)
        dashboard.charts = []
      })
    }
  },

  // Helpers
  _loadDashboards: function (campaigns, dashboards, offices) {
    var allDashboards = builtins.concat(_(dashboards.objects).sortBy('id').reverse().value())

    campaigns = _(campaigns)

    // Take the first location alphabetically at the highest geographic level
    // available as the default location for this dashboard
    // var office = _.min(offices, _.property('id'))

    this.dashboards = _(allDashboards)
      .map(function (d) {
        // Find the latest campaign for the chosen location
        // var campaign = campaigns
        //   .filter(c => {
        //     return office.id === c.office_id
        //   })
        //   .max(c => {
        //     return moment(c.start_date, 'YYYY-MM-DD').valueOf()
        //   })

        // Patch the non-comformant API response
        d.charts = d.charts || d.dashboard_json
        return d
      })
      .reject(_.isNull)
      .value()

    var indexedOffices = _.indexBy(offices, 'id')
    this.campaigns = campaigns
      .map(c => {
        var m = moment(c.start_date, 'YYYY-MM-DD')
        var dt = m.format('YYYY/MM')
        var officeName = indexedOffices[c.office_id].name
        var title = officeName + ': ' + m.format('MMMM YYYY')

        var links = _.map(allDashboards, function (d) {
          return _.defaults({
            path: _.kebabCase(d.title) + '/' + officeName + '/' + dt
          }, d)
        })

        return _.defaults({
          title: title,
          dashboards: links
        }, c)
      })

    this.loaded = true

    this.trigger({
      dashboards: this.dashboards,
      campaigns: this.campaigns,
      loaded: this.loaded
    })
  }
})

export default NavigationStore
