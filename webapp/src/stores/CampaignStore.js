'use strict';

var Reflux = require('reflux');
var api = require('data/api');

var CampaignStore = Reflux.createStore({
  init() {
    this.campaigns = api.campaign()
    	.then(data => {
        return data.objects;
      });
  },

  // API
  getCampaigns() {
    return this.campaigns;
  }
});

module.exports = CampaignStore;
