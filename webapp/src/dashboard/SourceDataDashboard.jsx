'use strict'

var _ = require('lodash')
var React = require('react')
var api = require('data/api.js')
var moment = require('moment')
var page = require('page')
var Reflux = require('reflux')

var NavigationStore = require('stores/NavigationStore')
var ReviewTable = require('dashboard/sd/ReviewTable.js')
var DocOverview = require('dashboard/sd/DocOverview.jsx')
var DocForm = require('dashboard/sd/DocForm.jsx')
var SourceDataDashboardStore = require('stores/SourceDataDashboardStore')
var SourceDataDashboardAction = require('actions/SourceDataDashboardActions')

var TitleMenu = require('component/TitleMenu.jsx')
var MenuItem = require('component/MenuItem.jsx')
var ReactCSSTransitionGroup = require('react/lib/ReactCSSTransitionGroup')

var {
  Datascope, LocalDatascope,
  SimpleDataTable, SimpleDataTableColumn,
  Paginator, SearchBar,
  FilterPanel, FilterDateRange
  } = require('react-datascope')

var SourceDataDashboard = React.createClass({
  mixins : [
    Reflux.connect(SourceDataDashboardStore)
  ],

  propTypes: {
    dashboard: React.PropTypes.object.isRequired,
    data: React.PropTypes.object.isRequired,
    location: React.PropTypes.object.isRequired,
    locations: React.PropTypes.object.isRequired,
    doc_id: React.PropTypes.number.isRequired,
    doc_tab: React.PropTypes.string.isRequired,

    loading: React.PropTypes.bool
  },

  getInitialState: function () {
    return {
      doc_obj: null
    }
  },

  componentWillMount: function (nextProps, nextState) {
    var data = SourceDataDashboardAction.getDocObj(this.props.doc_id)
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
      return <div className='admin-loading'> Source Dashboard Loading Loading...</div>
    }

    if (!doc_tab) {
      doc_tab = 'doc_index'
    }

    var docItems = MenuItem.fromArray(
      _.map(NavigationStore.documents, d => {
        return {
          title: d.doc_title,
          value: d.id
        }
      }),
      this._setDocId)

    var doc_tabs = MenuItem.fromArray(
      _.map(['viewraw', 'mapping', 'validate', 'results', 'doc_index'], d => {
        return {
          title: d,
          value: d
        }
      }),
      this._setDocTab)

    // navigation to set doc-id and doc-processor //
    var review_nav =
      <div className='admin-container'>
        <h1 className='admin-header'></h1>

        <div className='row'>
          <TitleMenu text={doc_obj.doc_title}>
            {docItems}
          </TitleMenu>
        </div>
        <div className='row'>
          <TitleMenu text={doc_tab}>
            {doc_tabs}
          </TitleMenu>
        </div>

      </div>

    const table_definition = {
      'viewraw': {
        'meta_fn': api.submissionMeta,
        'data_fn': api.submission,
        'fields': ['id', 'location_code', 'campaign_code', 'edit_link'],
        'search_fields': ['id', 'location_code', 'campaign_code']
      },
      'doc_index': {
        'data_fn': api.source_doc,
        'fields': ['id', 'doc_title', 'created_at', 'edit_link'],
        'search_fields': ['id', 'doc_title']
      },
      'mapping': {
        'data_fn': api.docMap,
        'fields': ['id', 'content_type', 'source_object_code', 'master_object_id', 'master_object_name', 'edit_link'],
        'search_fields': ['id', 'content_type', 'source_object_code', 'master_object_id', 'master_object_name']
      },
      'validate': {
        'data_fn': api.docDatapoint,
        'fields': ['id', 'document_id', 'location_id', 'indicator_id', 'campaign_id', 'value', 'edit_link'],
        'search_fields': ['location_id', 'indicator_id', 'campaign_id']
      },
      'results': {
        'data_fn': api.docResults,
        'fields': ['indicator_id', 'indicator__short_name', 'value'],
        'search_fields': ['indicator_id', 'indicator__short_name', 'value']
      }
    }

    var search_fields = table_definition[doc_tab]['search_fields']
    var datascopeFilters =
      <div>
        <SearchBar
          fieldNames={search_fields}
          placeholder='search ...'
          />
      </div>

    var table_key = _.kebabCase(this.props.location.name) + this.props.campaign.slug + doc_id + doc_tab
    // data table //
    var review_table = <ReviewTable
      title='sample title'
      getData={table_definition[doc_tab]['data_fn']}
      fields={table_definition[doc_tab]['fields']}
      location={location}
      key={table_key}
      loading={loading}
      doc_id={doc_id}
      doc_tab={doc_tab}
      campaign={campaign}
      datascopeFilters={datascopeFilters}
      >
      <Paginator />
      <SimpleDataTable>
        {table_definition[doc_tab]['fields'].map(fieldName => {
          return <SimpleDataTableColumn name={fieldName}/>
        })}
      </SimpleDataTable>
    </ReviewTable>

    var docForm
    var review_breakdown
    if (doc_tab === 'doc_index') {
      docForm = <div><DocForm></DocForm></div>
      review_breakdown = ''
    } else {
      docForm = ''
      review_breakdown = <DocOverview
        key={table_key + 'breakdown'}
        loading={loading}
        doc_id={doc_id}
        >
      </DocOverview>
    }

    var page_title = doc_obj.doc_title + ' - ' + doc_tab

    return (
      <div>
        {docForm}
        <div className='row'>
          <div id='popUp'></div>
          <div className='medium-9 columns'>
            <h2 style={{ textAlign: 'center' }} className='ufadmin-page-heading'>{page_title} </h2>
            {review_table}
          </div>
          <div className='medium-3 columns'>
            {review_nav}
            {review_breakdown}
          </div>
        </div>
      </div>)
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

module.exports = SourceDataDashboard
