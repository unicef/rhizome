import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import DatapointActions from 'actions/DatapointActions'

var DatapointStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: DatapointActions,

  datapoints: {
    meta: null,
    raw: null
  },

  getInitialState () {
    return this.datapoints
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
    this.setState(this.datapoints)
  },
  onFetchDatapointsFailed (error) {
    this.setState({ error: error })
  }
})

export default DatapointStore
