'use strict';

var _ = require('lodash');
var api = require('data/api');
var Reflux = require('reflux');

var MapFormStore = Reflux.createStore({

    listenables: [require('actions/MapFormActions')],

    init: function () {
        this.data = {
            modalIsOpen: false,
            master_object_id: null
        };
    },

    onOpenModal: function (id) {
        var self = this;

        api.get_source_object_map(id)
            .then(response => {
                self.data.modalIsOpen = true;
                self.data.source_object_code = response.objects[0].source_object_code;
                self.data.content_type = response.objects[0].content_type;
                self.trigger(self.data);
            });

    },

    onUpdateMetaMap: function (info) {
        var self = this;

        api.post_source_object_map(info).then(response => {
            self.data.master_object_id = response.objects.master_object_id;
            self.trigger(self.data);
        });
    }
});

module.exports = MapFormStore;
