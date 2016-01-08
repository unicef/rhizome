import _ from 'lodash'
import Reflux from 'reflux'
import api from 'data/api'

var UserGroupStore = Reflux.createStore({
  listenables: [require('actions/UserGroupActions')],

  data: {
    userGroups: []
  },

  getInitialState: function () {
    return this.data
  },

  onGetUserGroupByUserId: function (userId) {
    api.groups().then(response => {
      let groups = response.objects
      api.user_permissions({'user_id': userId}, null, {'cache-control': 'no-cache'})
        .then(data => {
          _.forEach(groups, function (group) {
            group.active = _.some(data.objects, {'group_id': group.id})
          })
          this.data.userGroups = response.objects
          this.trigger(this.data)
        })
    })
  }
})

export default UserGroupStore
