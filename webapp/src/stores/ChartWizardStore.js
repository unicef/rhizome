import Reflux from 'reflux'
import _ from 'lodash'

import ChartWizardActions from 'actions/ChartWizardActions'
import api from 'data/api'

let ChartWizardStore = Reflux.createStore({
  listenables: ChartWizardActions,
  data: {
    indicatorList: []
  },

  getInitialState() {
    return this.data
  },

  onInitialize() {
    api.indicatorsTree().then(data => {
      this.data.indicatorList = _(data.objects)
        .sortBy('title')
        .value()
      this.trigger(this.data)
    })
  }
})

export default ChartWizardStore
