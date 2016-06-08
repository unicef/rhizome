import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000/api/v1/'
axios.defaults.headers.common['Authorization'] = 'ApiKey fe_app:36cbe8cf3e07f1ce9f484f5320d2e4b95871f24d'

const RhizomeAPI = {
  get: (path, data) => axios.get(path, data),
  post: (path, data) => axios.post(path, data),
  put: (path, data) => axios.post(path, data),
  patch: (path, data) => axios.post(path, data)
}

export default RhizomeAPI
