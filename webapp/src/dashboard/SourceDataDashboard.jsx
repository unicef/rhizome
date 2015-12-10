import _ from 'lodash'
import React from 'react'
import api from 'data/api.js'
import moment from 'moment'
import page from 'page'
import Reflux from 'reflux'

// import ReviewTable from 'dashboard/sd/ReviewTable.js'
import DocOverview from 'dashboard/sd/DocOverview.jsx'
import DocForm from 'dashboard/sd/DocForm.jsx'
import SourceDataDashboardStore from 'stores/SourceDataDashboardStore'
import SourceDataDashboardActions from 'actions/SourceDataDashboardActions'

import CSVMenuItem from 'component/CSVMenuItem.jsx'

var {
  SimpleDataTable, SimpleDataTableColumn,
  Paginator, SearchBar
} = require('react-datascope')

var SourceDataDashboard = React.createClass({
  mixins: [
    Reflux.connect(SourceDataDashboardStore)
  ],

  propTypes: {
    dashboard: React.PropTypes.object.isRequired,
    data: React.PropTypes.object.isRequired,
    location: React.PropTypes.object.isRequired,
    locations: React.PropTypes.object.isRequired,
    doc_id: React.PropTypes.number.isRequired,
    doc_tab: React.PropTypes.string.isRequired,
    campaign: React.PropTypes.object,
    loading: React.PropTypes.bool
  },

  getInitialState: function () {
    return {
      doc_obj: null
    }
  },

  componentWillMount: function (nextProps, nextState) {
    var data = SourceDataDashboardActions.getDocObj(this.props.doc_id)
    this.setState({doc_obj: data.doc_obj})
  },

  componentWillUpdate: function (nextProps, nextState) {
    if (nextProps.doc_id !== this.props.doc_id) {
      return
    }
  },

  render: function () {
    var loading = this.props.loading
    var campaign = this.props.campaign
    var location = this.props.location
    var doc_id = this.props.doc_id
    var doc_tab = this.props.doc_tab

    var doc_obj = this.state.doc_obj

    if (!doc_obj) {
      return <div className='admin-loading'> Source Dashboard Loading...</div>
    }

    if (!doc_tab) {
      doc_tab = 'doc_index'
    }

    var doc_tabs = CSVMenuItem.fromArray(
      _.map(['viewraw', 'mapping', 'validate', 'results', 'doc_index'], d => {
        return {
          title: d,
          value: d
        }
      }),
      this._setDocTab)

    const table_definition = {
      'viewraw': {
        'meta_fn': api.submissionMeta,
        'data_fn': api.submission,
        'fields': ['id', 'location_code', 'campaign_code', 'edit_link'],
        'header': ['id', 'location_code', 'campaign_code', 'edit_link'],
        'search_fields': ['id', 'location_code', 'campaign_code']
      },
      'doc_index': {
        'data_fn': api.source_doc,
        'fields': ['id', 'doc_title', 'created_at', 'edit_link'],
        'header': ['id', 'doc_title', 'created_at', 'edit_link'],
        'search_fields': ['id', 'doc_title']
      },
      'mapping': {
        'data_fn': api.docMap,
        'fields': ['id', 'content_type', 'source_object_code', 'master_object_id', 'master_object_name', 'edit_link'],
        'header': ['id', 'content_type', 'source_object_code', 'master_object_id', 'master_object_name', 'edit_link'],
        'search_fields': ['id', 'content_type', 'source_object_code', 'master_object_id', 'master_object_name']
      },
      'validate': {
        'data_fn': api.docDatapoint,
        'fields': ['location__name', 'indicator__short_name', 'campaign__slug', 'value', 'edit_link'],
        'header': ['location', 'indicator', 'campaign', 'value', 'is valid'],
        'search_fields': ['location', 'indicator', 'campaign', 'value']
      },
      'results': {
        'data_fn': api.docResults,
        'fields': ['indicator_id', 'indicator__short_name', 'value'],
        'header': ['indicator_id', 'indicator__short_name', 'value'],
        'search_fields': ['indicator_id', 'indicator__short_name', 'value']
      }
    }

    var search_fields = table_definition[doc_tab]['search_fields']
    var datascopeFilters =
      (<div>
        <SearchBar
          fieldNames={search_fields}
          placeholder='Search for uploaded data'
          />
      </div>)

    var table_key = _.kebabCase(this.props.location.name) + this.props.campaign.slug + doc_id + doc_tab

    // data table //
    var review_table = '';
    // var review_table = (<ReviewTable
    //   title='sample title'
    //   getData={table_definition[doc_tab]['data_fn']}
    //   fields={table_definition[doc_tab]['fields']}
    //   header={table_definition[doc_tab]['header']}
    //   location={location}
    //   key={table_key}
    //   loading={loading}
    //   doc_id={doc_id}
    //   doc_tab={doc_tab}
    //   campaign={campaign}
    //   datascopeFilters={datascopeFilters}>
    //   <Paginator />
    //   <SimpleDataTable>
    //     {table_definition[doc_tab]['fields'].map(fieldName => {
    //       return <SimpleDataTableColumn name={fieldName}/>
    //     })}
    //   </SimpleDataTable>
    // </ReviewTable>)

    var uploadData = (
      <div>
        <div className='medium-12 columns upload__csv--load'>
          upload data
        </div>
        <DocForm
          campaign={this.props.campaign}
          location={this.props.location}
          doc_title = {doc_obj.doc_title}
          reviewTable={review_table}/>
      </div>
    )

    let tableMarginStyle = {
      marginTop: '50px'
    }

    var reviewData = (
      <div>
        <div className='medium-12 columns upload__csv--load'>
          Review Data
        </div>
        <div className='medium-12 columns upload__csv--step'>
          You can review raw data, map indicators, validate data and view results.
        </div>
        <div>
          <DocOverview
            key={table_key + 'breakdown'}
            loading={loading}
            doc_id={doc_id}
            doc_title={doc_obj.doc_title}/>
        </div>
        <div className='large-6 medium-12 small-12 columns csv-upload__title' style={tableMarginStyle}>
          {doc_tabs}
        </div>
        <hr />
        <div className='medium-12 columns'>
          {review_table}
        </div>
      </div>
    )

    var docForm = doc_tab === 'doc_index' ? uploadData : reviewData

    return (
      <div className='row upload__csv'>
        {docForm}
      </div>
    )
  },

  _setDocId: function (doc_id) {
    this._navigate({doc_id: doc_id})
    this.forceUpdate()
  },

  _setDocTab: function (doc_tab) {
    this._navigate({doc_tab: doc_tab})
    this.forceUpdate()
  },

  _navigate: function (params) {
    var slug = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title))
    var location = _.get(params, 'location', this.props.location.name)
    var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'))
    var doc_tab = _.get(params, 'doc_tab', this.props.doc_tab)
    var doc_id = _.get(params, 'doc_id', this.props.doc_id)

    if (_.isNumber(location)) {
      location = _.find(this.state.locations, r => r.id === location).name
    }

    page('/datapoints/' + [slug, location, campaign].join('/') + '/' + doc_tab + '/' + doc_id)
  }
})

export default SourceDataDashboard
