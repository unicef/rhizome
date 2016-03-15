import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import DatapointActions from 'actions/DatapointActions'

var DatapointStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: DatapointActions,

  datapoints: {
    meta: null,
    raw: null,
    index: null
  },

  getInitialState () {
    return this.datapoints
  },

  onRootStore (store) {
    this.campaignIndex = store.campaignIndex
    this.chartIndex = store.chartIndex
    this.locationIndex = store.locationIndex
    this.indicatorIndex = store.indicatorIndex
    this.officeIndex = store.officeIndex
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ============================  Fetch  Datapoints  ========================== //
  onFetchDatapoints () {
    this.setState({ raw: [] })
  },
  onFetchDatapointsCompleted (response) {
    this.datapoints.meta = response.meta
    this.datapoints.raw = response.objects
    this.datapoints.index = _.indexBy(this.datapoints.raw, 'id')
    this.setState(this.datapoints)
  },
  onFetchDatapointsFailed (error) {
    this.setState({ error: error })
  }
})

export default DatapointStore
