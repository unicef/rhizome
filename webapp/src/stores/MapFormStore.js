'use strict'

var _ = require('lodash')
var api = require('data/api')
var Reflux = require('reflux')

var MapFormStore = Reflux.createStore({
    init: function () {},

    getSourceMap: function (id) {
        return api.get_source_object_map(id, null, {'cache-control': 'no-cache'})
            .then(function (response) {
                return response.objects[0]
            })
    },

    updateMetaMap: function (info) {
        return api.post_source_object_map(info).then(function (response) {
            return response.objects.master_object_id
        })
    }
})

module.exports = MapFormStore
