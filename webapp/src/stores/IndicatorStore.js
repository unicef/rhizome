import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import IndicatorActions from 'actions/IndicatorActions'

var IndicatorStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: IndicatorActions,

  init () {
    IndicatorActions.fetchIndicators()
  },

  getInitialState () {
    return {
      indicatorIndex: []
    }
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ===============================  Fetch Indicators  ============================= //

  onFetchIndicators () {
    this.setState({ indicatorIndex: [] })
  },
  onFetchIndicatorsCompleted (response) {
    this.setState({ indicatorIndex: response })
  },
  onFetchIndicatorsFailed (error) {
    this.setState({ indicatorIndex: error })
  }
})

export default IndicatorStore
