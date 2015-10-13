'use strict';

var _ = require('lodash');
var api = require('data/api');
var Reflux = require('reflux');

var DocOverviewStore = Reflux.createStore({

    listenables: [require('actions/DocOverviewActions')],

    init: function () {
        this.data = {
            doc_id: null,
            doc_title: null,
            doc_detail_types: null,
            doc_deets: null
        };
    },

    onGetDocDetailTypes: function () {
        var self = this;
        api.docDetailType()
            .then(response => {
                self.data.doc_detail_types = response.objects;
                self.trigger(self.data);
            });
    },

    onRefreshMaster: function (document) {
        var self = this;
        api.refresh_master(document, null, {'cache-control': 'no-cache'})
            .then(response => {
                self.data.doc_deets = response.objects;
                self.trigger(self.data);
            });
    }
});

module.exports = DocOverviewStore;
