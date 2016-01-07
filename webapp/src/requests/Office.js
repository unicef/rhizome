import api from 'data/api'

export default {
  getOffices () {
    return api.office(null, null, {'cache-control': 'max-age=604800, public'}).then(response => {
      return response.objects
    })
  },
  getHomePageCharts () {
    return api.office({'is_homepage': 1}, null, {'cache-control': 'max-age=604800, public'}).then(response => {
      return response.objects
    })
  }
}
