import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import DatapointActions from 'actions/DatapointActions'

var DatapointStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: DatapointActions,

  datapoints: {
    meta: null,
    melted: null,
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
    this.setState({
      meta: response.meta,
      raw: response.objects,
      melted: _(response.objects)
        .flatten()
        .sortBy(_.method('campaign.start_date.getTime'))
        .map(this.melt)
        .flatten()
        .value()
    })
  },

  onFetchDatapointsFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                                  UTILITIES                                  //
  // =========================================================================== //
  melt (datapoint) {
    var base = _.omit(datapoint, 'indicators')
    return datapoint.indicators.map(indicator => {
      return _.assign({
        computed: indicator.computed,
        indicator: indicator.indicator,
        value: indicator.value
      }, base)
    })
  }
})

export default DatapointStore
