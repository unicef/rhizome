import _ from 'lodash'
import Reflux from 'reflux'
import React from 'react'

import DocOverviewActions from 'actions/DocOverviewActions'
import DocOverviewStore from 'stores/DocOverviewStore'

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
    this.pullDocDetailTypes()
    this.refreshMaster()
  },

  componentWillUpdate (nextProps, nextState) {
    if (nextProps.doc_id !== this.props.doc_id) {
      return
    }
  },

  pullDocDetailTypes () {
    DocOverviewActions.getDocDetailTypes()
  },

  refreshMaster () {
    var self = this
    DocOverviewActions.refreshMaster({document_id: self.props.doc_id})
  },

  queueReprocess () {
    var self = this
    DocOverviewActions.queueReprocess({document_id: self.props.doc_id})
  },

  renderLoading () {
    return <div className='admin-loading'> Doc Details Loading...</div>
  },

  render () {
    var doc_deets = this.state.doc_deets

    if (!doc_deets) return this.renderLoading()

    var refresh_master_btn = (<div>
      <p>
        <button disabled={this.state.isProcessing} className='tiny' className='large-3 medium-3 small-12 columns'
                onClick={this.queueReprocess}> { this.state.isProcessing ? 'Refreshing' : 'Refresh Reprocess'}
        </button>
      </p>
      <p>
        <button disabled={this.state.isRefreshing} className='tiny' className='large-3 medium-3 small-12 columns'
                onClick={this.refreshMaster}> { this.state.isRefreshing ? 'Refreshing' : 'Refresh Master'}
        </button>
      </p>
    </div>)

    var doc_detail_type_lookup = _.indexBy(this.state.doc_detail_types, 'id')
    var [doc_name, doc_revision] = this.props.doc_title.split('-')

    var rows = [
      <div className='large-6 medium-6 small-12 columns csv-upload__tags'>
        <span className='csv-upload__tags--span'>File_name: </span>{doc_name}
      </div>,
      <div className='large-6 medium-6 small-12 columns csv-upload__tags'>
        <span className='csv-upload__tags--span'>Revision: </span>{doc_revision}
      </div>
    ]

    for (var i = 0; i < doc_deets.length; i++) {
      var doc_detail = doc_deets[i]
      rows.push(
        <div className='large-6 medium-6 small-12 columns csv-upload__tags'>
          <span className='csv-upload__tags--span'>{doc_detail_type_lookup[doc_detail.doc_detail_type_id].name}: </span>
        {doc_detail.doc_detail_value}
        </div>)
    }

    return <div className='row csv-upload__message'>
      {rows}
      {refresh_master_btn}
    </div>
  }
})

export default DocOverview
