import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
// import page from 'page'
// import moment from 'moment'

// import randomHash from 'utilities/randomHash'

// import builtins from 'components/organisms/dashboard/builtin'
import ReviewTable from 'components/organisms/dashboard/sd/ReviewTable.js'
import DocForm from 'components/organisms/dashboard/sd/DocForm.jsx'
import DocOverview from 'components/organisms/dashboard/sd/DocOverview.jsx'

import CSVMenuItem from 'components/molecules/CSVMenuItem.jsx'

// import api from 'data/api'
// import DashboardAPI from 'data/requests/DashboardAPI'
// import DashboardInit from 'data/dashboardInit'

// import DashboardStoreOld from 'stores/DashboardStoreOld'
// import DataStore from 'stores/DataStore'
// import GeoStore from 'stores/GeoStore'
// import NavigationStore from 'stores/NavigationStore'

// import DashboardActions from 'actions/DashboardActions'
// import DataActions from 'actions/DataActions'
// import GeoActions from 'actions/GeoActions'

import SourceDataStore from 'stores/SourceDataStore'
// import SourceDataActions from 'actions/SourceDataActions'

var {
  SimpleDataTable, SimpleDataTableColumn,
  Paginator, SearchBar
} = require('react-datascope')

var SourceData = React.createClass({
  mixins: [
    Reflux.connect(SourceDataStore)
  ],

  // var loading = this.props.loading
  // var doc_id = this.props.doc_id
  render () {
    // if (this.state.loading) {
    //   let style = {
    //     fontSize: '2rem',
    //     zIndex: 9999
    //   }
    //
    //   return (
    //     <div style={style} className='overlay'>
    //       <div>
    //         <div><i className='fa fa-spinner fa-spin'></i>&ensp;Loading</div>
    //       </div>
    //     </div>
    //   )

    // } // END OF LOADING CONDITION //

    var table_definition = this.state.tableDef
    var doc_tab = this.state.doc_tab || 'doc_index'
    var doc_id = 2
    var doc_tabs = CSVMenuItem.fromArray(
      _.map(['viewraw', 'meta-data', 'results', 'doc_index'], d => {
        return {
          title: d,
          value: d
        }
      }),
      this._setDocTab)

    var search_fields = table_definition[doc_tab]['search_fields']
    var datascopeFilters = <SearchBar fieldNames={search_fields} placeholder='Search for uploaded data' />
    var table_key = doc_id + '-' + doc_tab

    // data table //

    var review_table = (<ReviewTable
      title='sample title' // sup w this
      getData={table_definition[doc_tab]['data_fn']}
      fields={table_definition[doc_tab]['fields']}
      header={table_definition[doc_tab]['header']}
      key={table_key}
      doc_id={doc_id}
      doc_tab={doc_tab}
      datascopeFilters={datascopeFilters}>
      <Paginator />
      <SimpleDataTable>
        {table_definition[doc_tab]['fields'].map(fieldName => {
          return <SimpleDataTableColumn name={fieldName}/>
        })}
      </SimpleDataTable>
    </ReviewTable>)

    var uploadData = (
      <div>
        <div className='medium-12 columns upload__csv--load'>
          upload data
        </div>
      </div>
    )
    // <DocForm
    //   doc_title = 'something'
    //   reviewTable={review_table}/>

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
              doc_id={doc_id}
              doc_title='something'/>
        </div>
        <div className='large-8 medium-12 small-12 columns csv-upload__title'>
          {doc_tabs}
        </div>
        <hr />
      </div>
    )

    // if it is doc index, then show the upload component, else show the doc review //
    var docForm = doc_tab === 'doc_index' ? uploadData : reviewData

    // return (
    //   <div className='row upload__csv'>
    //     {docForm}
    //   </div>
    // )
    // },

    return (
      <div>
        <div>
          {docForm}
        </div>
        <div className='medium-12 columns'>
          {review_table}
        </div>
    </div>

    )
  }
})

export default SourceData

//
// var doc_obj = this.state.doc_obj
// if (!doc_obj) {
//   return <div className='admin-loading'> Source Dashboard Loading...</div>
// }
//
// if (!doc_tab) {
//   doc_tab = 'doc_index'
// }
//
// var doc_tabs = CSVMenuItem.fromArray(
//   // _.map(['viewraw', 'results', 'doc_index'], d => {
//   _.map(['viewraw', 'meta-data', 'results', 'errors', 'doc_index'], d => {
//     return {
//       title: d,
//       value: d
//     }
//   }),
//   this._setDocTab)
//
//
//
// _setDocId: function (doc_id) {
// this._navigate({doc_id: doc_id})
// this.forceUpdate()
// },
//
// _setDocTab: function (doc_tab) {
// this._navigate({doc_tab: doc_tab})
// this.forceUpdate()
// },
//
// _navigate: function (params) {
// var slug = _.get(params, 'dashboard', _.kebabCase(this.props.dashboard.title))
// var location = _.get(params, 'location', this.props.location.name)
// var campaign = _.get(params, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'))
// var doc_tab = _.get(params, 'doc_tab', this.props.doc_tab)
// var doc_id = _.get(params, 'doc_id', this.props.doc_id)
//
// if (_.isNumber(location)) {
//   location = _.find(this.state.locations, r => r.id === location).name
// }
//
// page('/' + [slug, location, campaign].join('/') + '/' + doc_tab + '/' + doc_id)
// }
// })
