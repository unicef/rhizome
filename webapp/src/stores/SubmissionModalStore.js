'use strict';

var _ = require('lodash');
var api = require('data/api');
var Reflux = require('reflux');

var SubmissionModalStore = Reflux.createStore({

    listenables: [require('actions/SubmissionModalActions')],

    init: function () {
        this.data = {
            modalIsOpen: false,
            source_submission_id: null,
            submission_data: null
        };
    },

    onOpenModel: function (id) {
        var self = this;
        api.submission(id)
            .then(response => {
                self.data.submission_data = response.objects[0];
                self.trigger(self.data);
            });
    }
});

module.exports = SubmissionModalStore;
