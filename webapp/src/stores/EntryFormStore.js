import Reflux from 'reflux'

let EntryFormStore = Reflux.createStore({
  listenables: [require('actions/EntryFormActions')],

  data: {
    indicationSelected: 2
  },

  getInitialState: function () {
    return this.data
  },

  onSetIndicator: function (optionId) {
    this.data.indicationSelected = optionId
    this.trigger(this.data)
  }
})

export default EntryFormStore
