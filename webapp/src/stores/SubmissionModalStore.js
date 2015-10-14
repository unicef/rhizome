'use strict';

var _ = require('lodash');
var api = require('data/api');
var Reflux = require('reflux');

var SubmissionModalStore = Reflux.createStore({

    listenables: [require('actions/SubmissionModalActions')],

    init: function () {
    },

    onGetSubmission: function (id) {
        return api.submission(id)
            .then(response => {
                return response.objects[0];
            });
    }
});

module.exports = SubmissionModalStore;
