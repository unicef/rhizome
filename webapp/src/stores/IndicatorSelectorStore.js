import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import IndicatorSelectorActions from 'actions/IndicatorSelectorActions'
import IndicatorStore from 'stores/IndicatorStore'

const IndicatorSelectorStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: IndicatorSelectorActions,

  indicators: [],

  selected_indicators: [],

  getInitialState () {
    return this.selected_indicators
  },

  init () {
    this.listenTo(IndicatorStore, this.onIndicatorStore)
  },

  onIndicatorStore (store) {
    this.indicators = store
  },

  onSelectIndicator (id) {
    this.selected_indicators.push(this.indicators.index[id])
    this.trigger(this.selected_indicators)
  },

  onDeselectIndicator (id) {
    _.remove(this.selected_indicators, {id: id})
    this.trigger(this.selected_indicators)
  },

  onReorderIndicator (selected_indicators) {
    this.selected_indicators = selected_indicators
    this.trigger(this.selected_indicators)
  },

  onSetSelectedIndicators (ids) {
    if (Array.isArray(ids)) {
      this.selected_indicators = ids.map(id => this.indicators.index[id])
    } else {
      this.selected_indicators = [this.indicators.index[ids]]
    }
    this.trigger(this.selected_indicators)
  },

  onClearSelectedIndicators () {
    this.selected_indicators = []
    this.trigger(this.selected_indicators)
  }
})

export default IndicatorSelectorStore
