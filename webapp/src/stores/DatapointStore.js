import _ from 'lodash'
import moment from 'moment'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import CampaignStore from 'stores/CampaignStore'
import IndicatorStore from 'stores/IndicatorStore'
import LocationStore from 'stores/LocationStore'

import DatapointActions from 'actions/DatapointActions'

var DatapointStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: DatapointActions,

  datapoints: {
    meta: null,
    raw: null,
    flattened: null,
    grouped: null,
    melted: null
  },

  init: function () {
    this.joinTrailing(LocationStore, IndicatorStore, CampaignStore, this.onGetInintialStores)
  },

  onGetInintialStores: function (locations, indicators, campaigns) {
    this.indicators = indicators[0]
    this.locations = locations[0]
    this.campaigns = campaigns[0]
  },

  getInitialState: function () {
    return this.datapoints
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ============================  Fetch  Datapoints  ========================== //
  onFetchDatapoints: function () {
    this.setState({ raw: null, meta: null, grouped: null, flattened: null, melted: null })
  },
  onFetchDatapointsCompleted: function (response) {
    const datapoints = {
      meta: response.meta,
      raw: response.objects,
      flattened: this.flatten(response.objects),
      melted: this.melt(response.objects, response.meta.indicator_ids)
    }
    datapoints.grouped = _.groupBy(datapoints.flattened, 'campaign.id')
    this.setState(datapoints)
  },
  onFetchDatapointsFailed: function (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onClearDatapoints: function () {
    this.setState({ raw: null, meta: null, flattened: null, melted: null })
  },

  // =========================================================================== //
  //                                  UTILITIES                                  //
  // =========================================================================== //
  flatten: function (datapoints) {
    const flattened = datapoints.map(d => {
      const indicator = this.indicators.index[d.indicator_id]
      const datapoint = {
        id: d.computed_id,
        value: d.value ? this._formatValue(d.value, indicator.data_format) : null,
        location: this.locations.index[d.location_id],
        indicator: indicator
      }
      if (d.data_date) { datapoint.data_date = d.data_date }
      if (d.campaign_id) {
        datapoint.campaign = this.campaigns.index[d.campaign_id] || this._createYearCampaign(d.campaign_id)
      }
      return datapoint
    })
    return flattened
  },

  _formatValue: function (value, data_format) {
    if (data_format === 'int' || data_format === 'pct') {
      return value === 0.0 || value === '0.0' ? 0 : parseFloat(value)
    } else if (data_format === 'date') {
      return moment(value, 'YYYY-MM-DD').toDate()
    } else {
      return value
    }
  },

  _createYearCampaign: function (year) {
    return {
      id: year,
      name: year,
      start_date: moment(year + '-01-01', 'YYYY-MM-DD').toDate(),
      end_date: moment(year + '-12-31', 'YYYY-MM-DD').toDate()
    }
  },

  melt: function (datapoints, indicator_ids) {
    const baseIndicators = indicator_ids.map(id => ({ indicator: parseInt(id, 0), value: 0 }))
    const melted_datapoints = _(datapoints).map(datapoint => {
      const base = _.omit(datapoint, 'indicators')
      const indicatorFullList = _.assign(_.cloneDeep(baseIndicators), datapoint.indicators)
      return indicatorFullList.map(indicator => _.assign({}, base, indicator))
    })
      .flatten()
      .value()
    melted_datapoints.forEach(melted_datapoint => {
      melted_datapoint.indicator = this.indicators.index[melted_datapoint.indicator]
      melted_datapoint.location = this.locations.index[melted_datapoint.location]
    })
    return melted_datapoints
  }

})

export default DatapointStore
