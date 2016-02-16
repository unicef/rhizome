import Reflux from 'reflux'
import React from 'react'
import api from 'data/api'

import DocOverviewActions from 'actions/DocOverviewActions'
import DocOverviewStore from 'stores/DocOverviewStore'
import DownloadButton from '02-molecules/DownloadButton.jsx'

var DocOverview = React.createClass({
  mixins: [
    Reflux.connect(DocOverviewStore)
  ],

  propTypes: {
    doc_id: React.PropTypes.number.isRequired,
    doc_tab: React.PropTypes.string.isRequired,
    loading: React.PropTypes.bool,
    doc_title: React.PropTypes.string
  },

  getDefaultProps () {
    return {
      loading: false
    }
  },

  getInitialState () {
    return {
      doc_id: null,
      doc_title: null,
      doc_detail_types: null,
      doc_deets: null,
      isRefreshing: false,
      isProcessing: false
    }
  },

  componentWillMount (nextProps, nextState) {
    this.pullDocDetails()
  },

  componentWillUpdate (nextProps, nextState) {
    if (nextProps.doc_id !== this.props.doc_id) {
      return
    }
  },

  pullDocDetails () {
    var self = this
    DocOverviewActions.getDocDetails(self.props.doc_id)
  },

  refreshMaster () {
    var self = this
    DocOverviewActions.refreshMaster({document_id: self.props.doc_id})
  },
  syncOdk () {
    var self = this
    DocOverviewActions.syncOdk({document_id: self.props.doc_id})
  },

  queueReprocess () {
    var self = this
    DocOverviewActions.queueReprocess({document_id: self.props.doc_id})
  },

  renderLoading () {
    return <div className='admin-loading'> Doc Details Loading...</div>
  },

  _download: function () {
    return api.submission.toString({'format': 'csv', 'document_id': this.props.doc_id})
  },

  render () {
    var doc_deets = this.state.doc_deets

    if (!doc_deets) return this.renderLoading()

    var [doc_name, doc_revision] = this.props.doc_title.split('-')

    var rows = [
      <div className='large-6 medium-6 small-12 columns csv-upload__tags'>
        <span className='csv-upload__tags--span'>File_name: </span>{doc_name}
      </div>,
      <div className='large-6 medium-6 small-12 columns csv-upload__tags'>
        <span className='csv-upload__tags--span'>Revision: </span>{doc_revision}
      </div>
    ]

    var odkRefreshBtn = <span>&nbsp;</span>

    for (var i = 0; i < doc_deets.length; i++) {
      var doc_detail = doc_deets[i]

      if (doc_detail.doc_detail_type__name === 'odk_form_name') {
        odkRefreshBtn = (
          <a disabled={this.state.isFetchingOdk} className='button button-refresh large-3 medium-3 small-12 columns'
             onClick={this.syncOdk}> { this.state.isFetchingOdk ? 'Refreshing' : 'Fetch ODK Data'}
          </a>
        )
      }

      rows.push(
        <div className='large-6 medium-6 small-12 columns csv-upload__tags'>
          <span className='csv-upload__tags--span'>{doc_detail.doc_detail_type__name}: </span>
          {doc_detail.doc_detail_value}
        </div>)
    }

    var button_row = (
      <div className='button-row small-12 columns'>
        <a disabled={this.state.isProcessing} className='button button-refresh large-3 medium-3 small-12 columns'
           onClick={this.queueReprocess}> { this.state.isProcessing ? 'Refreshing' : 'Queue For Reprocessing'}
        </a>
        <a disabled={this.state.isRefreshing} className='button button-refresh large-3 medium-3 small-12 columns'
           onClick={this.refreshMaster}> { this.state.isRefreshing ? 'Refreshing' : 'Refresh Master'}
        </a>
        <DownloadButton
          onClick={this._download}
          classes="large-3 medium-3 small-12 columns"
          enable='true'
          text='Download Raw'
          working='Downloading'
          cookieName='dataBrowserCsvDownload' />
        {odkRefreshBtn}
      </div>
    )

    return <div className='row csv-upload__message'>
      {rows}
      {button_row}
    </div>
  }
})

export default DocOverview