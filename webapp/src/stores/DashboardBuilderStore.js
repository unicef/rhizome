import _ from 'lodash'
import Reflux from 'reflux/src'

import api from 'data/api'
import randomHash from 'util/randomHash'

import DashboardActions from 'actions/DashboardActions'
import LayoutDefaultSettings from 'dashboard/builtin/layout-options.js'

var DashboardBuilderStore = Reflux.createStore({
  listenables: [require('actions/DashboardBuilderActions')],

  getInitialState () {
    return this.data
  },

  data: {
    loaded: false,
    newDashboard: false,
    dashboardTitle: '',
    dashboardDescription: '',
    layout: LayoutDefaultSettings.defaultValue
  },

  onInitialize (id) {
    this.dashboardId = id
    console.log('id: ', id)
    if (_.isNull(id)) {
      this.data.newDashboard = true
      this.data.loaded = true
      this.data.dashboard = {}
      this.data.dashboard.charts = []
      this.trigger(this.data)
    } else {
      api.get_dashboard({ id: id }, null, { 'cache-control': 'no-cache' }).then(dashboard => {
        this.data.dashboard = dashboard.objects[0]
        this.data.layout = dashboard.objects[0].layout
        this.data.loaded = true
        this.data.dashboardTitle = dashboard.objects[0].title
        this.data.dashboardDescription = dashboard.objects[0].description

        api.get_chart({ dashboard_id: id, _: randomHash() }, null, { 'cache-control': 'no-cache' }).then(res => {
          let charts = res.objects.map(chart => {
            let result = chart.chart_json
            result.id = chart.id
            return result
          })
          this.data.dashboard.charts = _.sortBy(charts, _.property('id'))
          DashboardActions.setDashboard({ dashboard: this.data.dashboard })
          this.trigger(this.data)
        }, err => {
          console.log(err)
          this.data.dashboard.charts = []
          this.trigger(this.data)
        })
      })
    }
  },

  onAddChart (chartDef) {
    // in this api do not need set the chart id.
    // chartDef.id = chartDef.title + (new Date()).valueOf()

    console.log('chartDef: ', chartDef)
    this.data.dashboard.charts.push(chartDef)
    DashboardActions.setDashboard({ dashboard: this.data.dashboard })

    // do not save the whole dashboard.
    // this.saveDashboard()

    // just save the chart.
    var data = {
      dashboard_id: this.dashboardId,
      chart_json: JSON.stringify(chartDef)
    }

    api.post_chart(data).then(res => {
      chartDef.id = res.objects.id
      this.trigger(this.data)
    }, res => {
      console.log('add chart error,', res)
      this.trigger(this.data)
    })
  },

  onRemoveChart (index) {
    var chart = this.data.dashboard.charts.splice(index, 1)[0]
    DashboardActions.setDashboard({ dashboard: this.data.dashboard })

    // do not save the whole dashboard.
    // this.saveDashboard()
    var data = {
      id: chart.id
    }

    api.delete_chart(data).then(res => {
      this.trigger(this.data)
    }, res => {
      console.log('remove chart error,', res)
      this.trigger(this.data)
    })
  },

  onMoveForward (index) {
    var newIndex
    if (index === this.data.dashboard.charts.length - 1) {
      newIndex = 0
    } else {
      newIndex = index + 1
    }
    var temp = this.data.dashboard.charts[index]
    this.data.dashboard.charts[index] = this.data.dashboard.charts[newIndex]
    this.data.dashboard.charts[newIndex] = temp
    this.saveDashboard()
    this.trigger(this.data)
  },

  onMoveBackward (index) {
    var newIndex
    if (index === 0) {
      newIndex = this.data.dashboard.charts.length - 1
    } else {
      newIndex = index - 1
    }
    var temp = this.data.dashboard.charts[index]
    this.data.dashboard.charts[index] = this.data.dashboard.charts[newIndex]
    this.data.dashboard.charts[newIndex] = temp
    this.saveDashboard()
    this.trigger(this.data)
  },

  onDeleteDashboard () {
    api.remove_dashboard({id: this.data.dashboard.id}).then(() => {
      window.location = '/datapoints/dashboards/'
    })
  },

  onAddDashboard () {
    var data = {
      title: this.data.dashboardTitle,
      description: '',
      default_office_id: null,
      dashboard_json: '[]',
      layout: this.data.layout
    }
    api.save_dashboard(data).then(res => {
      if (res.objects.id) {
        window.location = '/datapoints/dashboards/edit/' + res.objects.id
      } else {
        window.alert('There was an error saving your chart')
      }
    }, res => {
      window.alert(res.msg)
    })
  },
  saveDashboard () {
    var data = {
      id: this.data.dashboard.id,
      description: this.data.dashboardDescription,
      title: this.data.dashboardTitle,
      default_office_id: null,
      layout: this.data.layout,
      dashboard_json: JSON.stringify(this.data.dashboard.charts)
    }
    api.save_dashboard(data).then(() => {
    }, err => {
      console.log(err)
    })
  },

  onUpdateChart (chartDef, index) {
    this.data.dashboard.charts[index] = chartDef
    DashboardActions.setDashboard({ dashboard: this.data.dashboard })

    var data = {
      id: chartDef.id,
      chart_json: JSON.stringify(chartDef)
    }

    api.post_chart(data).then(res => {
      this.trigger(this.data)
    }, res => {
      console.log('update chart error,', res)
      this.trigger(this.data)
    })
  },

  onUpdateTitle (title) {
    this.data.dashboardTitle = title
    clearTimeout(this.timer)
    if (this.data.dashboard) {
      this.timer = setTimeout(function () {
        this.saveDashboard()
      }.bind(this), 1000)
    }
  },

  onUpdateDescription (description) {
    this.data.dashboardDescription = description
    clearTimeout(this.timer)
    this.timer = setTimeout(function () {
      this.saveDashboard()
    }.bind(this), 1000)
  },

  onChangeLayout (value) {
    this.data.layout = value
    this.trigger(this.data)
  }
})

export default DashboardBuilderStore
