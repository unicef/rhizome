import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import api from 'data/api'
import moment from 'moment'

import ExpandableSection from 'component/ExpandableSection.jsx'
import DateRangePicker from 'component/DateTimePicker.jsx'
import DropdownMenu from 'component/menus/DropdownMenu.jsx'
import DatabrowserTable from 'component/DatabrowserTable.jsx'
import List from 'component/list/List.jsx'
import ReorderableList from 'component/list/ReorderableList.jsx'
import DownloadButton from 'component/DownloadButton.jsx'

import ExplorerStore from 'stores/ExplorerStore'

import DataBrowserTableActions from 'actions/DataBrowserTableActions'
import ExplorerActions from 'actions/ExplorerActions'

let Explorer = React.createClass({
  mixins: [Reflux.connect(ExplorerStore)],

  componentWillMount: function () {
    ExplorerActions.getLocations()
    ExplorerActions.getIndicators()
  },

  _tableValueUpdate: function (data) {
    this.setState({hasData: data && data.length > 0})
  },

  refresh: function () {
    if (!this.state.couldLoad) return
    DataBrowserTableActions.getTableData(this.state.campaign, this.state.locationSelected, this.state.indicatorSelected)
  },

  _download: function () {
    let locations = _.map(this.state.locationSelected, 'id')
    let indicators = _.map(this.state.indicatorSelected, 'id')
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
            <from className='inline'>
              <ExpandableSection title='Locations' refer='preview'>
                <DropdownMenu items={this.state.locations} sendValue={ExplorerActions.addLocation} item_plural_name='Locations' text='Select Location' style='databrowser__button' icon='fa-globe'/>
                <List items={this.state.locationSelected} removeItem={ExplorerActions.removeLocation}/>
              </ExpandableSection>

              <ExpandableSection title='Indicators' refer='preview'>
                <DropdownMenu items={this.state.indicators} sendValue={ExplorerActions.addIndicators} item_plural_name='Indicators' text='Choose Indicators' style='databrowser__button'/>
                <ReorderableList items={this.state.indicatorSelected} removeItem={ExplorerActions.removeIndicator} dragItem={ExplorerActions.reorderIndicator}/>
              </ExpandableSection>

              <ExpandableSection title='Time Period' refer='preview'>
                <DateRangePicker sendValue={ExplorerActions.updateDateRangePicker} start={this.state.campaign.start} end={this.state.campaign.end} text='to' fromComponent='Explorer'/>
              </ExpandableSection>

              <a role='button' onClick={this.refresh} className={this.state.couldLoad ? 'button success' : 'button success disabled'} style={{marginTop: '21px'}}>
                <i className='fa fa-fw fa-refresh'/>&emsp;Load Data
              </a>
            </from>
          </div>
          <div className='medium-9 columns'>
            <DatabrowserTable updateValue={this._tableValueUpdate}/>
            <DownloadButton onClick={this._download} enable={this.state.hasData} text='Download All' working='Downloading' cookieName='dataBrowserCsvDownload'/>
          </div>
        </div>
      </div>
    )
  }
})

export default Explorer
