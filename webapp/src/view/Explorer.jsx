import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import api from 'data/api'
import moment from 'moment'

import ExpandableSection from 'component/ExpandableSection'
import DataFilters from './DataFilters'
import DateRangePicker from 'component/DateTimePicker'
import DropdownMenu from 'component/menus/DropdownMenu'
import DatabrowserTable from 'component/DatabrowserTable'
import List from 'component/list/List'
import ReorderableList from 'component/list/ReorderableList'
import DownloadButton from 'component/DownloadButton'

import DataBrowserTableActions from 'actions/DataBrowserTableActions'

let Explorer = React.createClass({

  getInitialState: function() {
    return {
      data: null,
      selected_locations: null,
      selected_indicators: null
    };
  },

  refresh: function (results) {
    this.setState(results)
  },

  _download: function () {
    let locations = _.map(this.state.selected_locations, 'id')
    let indicators = _.map(this.state.selected_indicators, 'id')
    let query = { 'format': 'csv' }

    if (indicators.length > 0) query.indicator__in = indicators
    if (locations.length > 0) query.location_id__in = locations
    if (this.state.campaign.start) query.campaign_start = moment(this.state.campaign.start).format('YYYY-M-D')
    if (this.state.campaign.end) query.campaign_end = moment(this.state.campaign.end).format('YYYY-M-D')

    return api.datapoints.toString(query)
  },

  render: function () {
    return (
      <div>
        <div className='row'>
          <div className='small-12 columns'>
            <h1 style={{textAlign: 'left'}}>Raw Data</h1>
          </div>
        </div>
        <div className='row'>
          <div className='medium-3 columns'>
            <DataFilters processResults={this.refresh}/>
          </div>
          <div className='medium-9 columns'>
            <DatabrowserTable data={this.state.data} selected_locations={this.state.selected_locations} selected_indicators={this.state.selected_indicators} />
            <DownloadButton onClick={this._download} enable={this.state.hasData} text='Download All' working='Downloading' cookieName='dataBrowserCsvDownload'/>
          </div>
        </div>
      </div>
    )
  }
})

export default Explorer
