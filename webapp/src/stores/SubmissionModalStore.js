'use strict'

var api = require('data/api')
var Reflux = require('reflux')

var SubmissionModalStore = Reflux.createStore({
  init: function () {},

  getSubmission: function (id) {
    return api.submission(id)
      .then(response => {
        return response.objects[0]
      })
  }
})

module.exports = SubmissionModalStore
