import api from 'data/api'
import Reflux from 'reflux'

var SubmissionModalStore = Reflux.createStore({
  init: function () {},

  getSubmission: function (id) {
    return api.submission(id)
      .then(response => {
        return response.objects[0]
      })
  }
})

export default SubmissionModalStore
