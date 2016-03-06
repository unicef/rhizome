import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import api from 'data/api'
import moment from 'moment'

import ExpandableSection from 'components/molecules/ExpandableSection'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import DateRangePicker from 'components/molecules/DateRangePicker'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DownloadButton from 'components/molecules/DownloadButton'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import List from 'components/molecules/list/List'

import DataFilters from 'components/organisms/DataFilters'

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
