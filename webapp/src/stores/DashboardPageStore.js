import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import DashboardPageActions from 'actions/DashboardPageActions'

const DashboardPageStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: [DashboardPageActions],

  getInitialState: () => {
    return {
      dashbaord: null
    }
  }
})

export default DashboardPageStore
