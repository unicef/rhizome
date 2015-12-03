import api from 'data/api'

export default {
  getLocations () {
    return api.locations(null, null, { 'cache-control': 'max-age=604800, public' }).then(response => {
      return response.objects
    })
  },

  getLocationTypes () {
    return api.location_type(null, null, { 'cache-control': 'max-age=604800, public' }).then(response => {
      return response.objects
    })
  }
}
