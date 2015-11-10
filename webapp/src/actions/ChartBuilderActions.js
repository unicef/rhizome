'use strict'

var Reflux = require('reflux')
// Each action is like an event channel for one specific event. Actions are called by components.
// The store is listening to all actions, and the components in turn are listening to the store.
// Thus the flow is: User interaction -> component calls action -> store reacts and triggers -> components update

module.exports = Reflux.createActions([
  'addIndicatorSelection',
  'removeIndicatorSelection',
  'updateTitle',
  'updateDescription',
  'selectShowLocationRadio',
  'selectGroupByRadio',
  'selectTimeRadio',
  'selectXFormatRadio',
  'selectFormatRadio',
  'selectChart',
  'addCampaignSelection',
  'addLocationSelection',
  'selectXAxis',
  'selectYAxis',
  'createChart',
  'initialize'
])
