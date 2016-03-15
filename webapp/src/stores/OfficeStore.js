import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import OfficeActions from 'actions/OfficeActions'

var OfficeStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: OfficeActions,

  init () {
    OfficeActions.fetchOffices()
  },

  offices: {
    meta: null,
    raw: null,
    index: null
  },

  getInitialState () {
    return this.offices
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ==============================  Fetch Offices  ============================ //
  onFetchOffices () {
    this.setState({ raw: [] })
  },
  onFetchOfficesCompleted (response) {
    this.setState({
      meta: response.meta,
      raw: response.objects,
      index: _.indexBy(response.objects, 'id')
    })
  },
  onFetchOfficesFailed (error) {
    this.setState({ error: error })
  }
})

export default OfficeStore
