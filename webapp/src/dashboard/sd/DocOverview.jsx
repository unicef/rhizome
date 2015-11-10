var _ = require('lodash')
var Reflux = require('reflux')
var React = require('react')

var DropdownMenu = require('component/DropdownMenu.jsx')
var NavigationStore = require('stores/NavigationStore')

var DocOverviewActions = require('actions/DocOverviewActions')
var DocOverviewStore = require('stores/DocOverviewStore')

var DocOverview = React.createClass({
  mixins: [
    Reflux.connect(DocOverviewStore)
  ],

  propTypes: {
    doc_id: React.PropTypes.number.isRequired,
    doc_tab: React.PropTypes.string.isRequired,
    loading: React.PropTypes.bool
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
    if (nextProps.doc_deets !== this.props.doc_deets) {
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
    var doc_id = this.props.doc_id
    var doc_tab = this.props.doc_tab
    var doc_deets = this.state.doc_deets

    if (!doc_deets) return this.renderLoading()

    var refresh_master_btn = <div>
      <p>
        <button disabled={this.state.isProcessing} className='tiny' onClick={this.queueReprocess}> { this.state.isProcessing ? 'To Reprocess...' : 'To Reprocess!'}
        </button>
      </p>
      <p>
        <button disabled={this.state.isRefreshing} className='tiny'
                onClick={this.refreshMaster}> { this.state.isRefreshing ? 'Refresh Master...' : 'Refresh Master!'}
        </button>
      </p>
    </div>

    var doc_detail_type_lookup = _.indexBy(this.state.doc_detail_types, 'id')

    var rows = []
    for (var i = 0; i < doc_deets.length; i++) {
      var doc_detail = doc_deets[i]
      rows.push(<li>{doc_detail_type_lookup[doc_detail.doc_detail_type_id].name}
        : {doc_detail.doc_detail_value} </li>)
    }

    return <div>

      <h3> Document Overview </h3>
      <ul>{rows}</ul>
      {refresh_master_btn}
    </div>
  }
})

module.exports = DocOverview
