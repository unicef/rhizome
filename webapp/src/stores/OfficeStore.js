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
    const offices = response.objects[0].offices || response.objects
    this.setState({
      meta: response.meta,
      raw: offices,
      index: _.indexBy(offices, 'id')
    })
  },
  onFetchOfficesFailed (error) {
    this.setState({ error: error })
  }
})

export default OfficeStore
