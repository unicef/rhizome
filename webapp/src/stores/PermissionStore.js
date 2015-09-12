'use strict';

var Reflux = require('reflux');
var api = require('data/api');

var PermissionStore = Reflux.createStore({
  init() {
    this.permissions = [];

    api.user_permissions()
      .then(data => {
        this.permissions = _.map(data.objects, p => p.auth_code);
        return this.permissions;
      });
  },

  getInitialState() {
    return {
      permissions: this.permissions,
    };
  },

  // API
  userHasPermission(permissionString) {
    console.log("userHasPermission:", permissionString, this.permissions.indexOf(permissionString.toLowerCase()) > -1);
    return this.permissions.indexOf(permissionString.toLowerCase()) > -1;
  }
});

module.exports = PermissionStore;
