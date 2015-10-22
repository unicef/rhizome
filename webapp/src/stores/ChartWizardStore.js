import Reflux from 'reflux'
import _ from 'lodash'

import ChartWizardActions from 'actions/ChartWizardActions'
import api from 'data/api'

let ChartWizardStore = Reflux.createStore({
  listenables: ChartWizardActions,
  data: {
    indicatorList: [],
    indicatorSelected: []
  },

  getInitialState() {
    return this.data
  },

  onInitialize(chartDef) {

    api.indicatorsTree().then(data => {
      this.indicatorIndex = _.indexBy(data.flat, 'id');
      this.data.indicatorList = _(data.objects)
        .sortBy('title')
        .value()
      this.data.indicatorSelected = chartDef.indicators.map(id => {
        return this.indicatorIndex[id]
      })
      this.trigger(this.data)
    })
  },

  onAddIndicator(index) {
    this.data.indicatorSelected.push(this.indicatorIndex[index])
    this.trigger(this.data)
  },

  onRemoveIndicator(id) {
    _.remove(this.data.indicatorSelected, {id: id});
	  this.trigger(this.data);
  }
})

export default ChartWizardStore
