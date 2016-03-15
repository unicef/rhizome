import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import OfficeActions from 'actions/OfficeActions'

var OfficeStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: OfficeActions,

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
    this.offices.meta = response.meta
    this.offices.raw = response.objects
    this.offices.index = _.indexBy(this.offices.raw, 'id')
    this.setState(this.offices)
  },
  onFetchOfficesFailed (error) {
    this.setState({ error: error })
  }
})

export default OfficeStore
