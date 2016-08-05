import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import page from 'page'

import ReviewTable from 'components/organisms/source-data/ReviewTable'
import DocOverview from 'components/organisms/source-data/DocOverview'
import CSVMenuItem from 'components/organisms/source-data/CSVMenuItem'
import DocForm from 'components/organisms/source-data/DocForm'

import SourceDataStore from 'stores/SourceDataStore'

import TableToRefactor from 'components/organisms/datascope/TableToRefactor'
import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
import Paginator from 'components/organisms/datascope/Paginator'
import SearchBar from 'components/organisms/datascope/SearchBar'

var SourceDataContainer = React.createClass({
  mixins: [
    Reflux.connect(SourceDataStore)
  ],

  _setDocId: function (doc_id) {
    page('/source-data/' + this.state.doc_tab + '/' + doc_id)
  },
  _setDocTab: function (doc_tab) {
    page('/source-data/' + doc_tab + '/' + this.state.doc_id)
  },

  componentWillMount () {
    // http://localhost:8000/source-data/viewraw/76 //
    let currentPath = window.location.pathname
    let cleanPath = currentPath.replace('/source-data/', '')
    let urlParams = cleanPath.split('/')

    let newState = {
      'doc_tab': 'doc_index',
      'doc_id': null
    }

    if (urlParams.length === 2) {
      newState = {
        'doc_tab': urlParams[0],
        'doc_id': urlParams[1]
      }
    }

    this.setState(newState)
  },

  render () {
    var table_definition = this.state.tableDef
    var doc_tab = this.state.doc_tab || 'doc_index'
    var doc_id = this.state.doc_id
    var file_type = this.state.file_type || null

    var docTabsAvailable = file_type === 'date' ?
      ['viewraw', 'mapped', 'un-mapped', 'date_results', 'doc_index'] :
      ['viewraw', 'mapped', 'un-mapped', 'campaign_results', 'doc_index']

    var doc_tabs = CSVMenuItem.fromArray(
      _.map(docTabsAvailable, d => {
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
      <TableToRefactor>
        {table_definition[doc_tab]['fields'].map(fieldName => {
          return <SimpleDataTableColumn name={fieldName}/>
        })}
      </TableToRefactor>
    </ReviewTable>)

    var uploadData = (
      <div>
        <div className='medium-12 columns upload__csv--load'>
          upload data
        </div>
        <DocForm/>
      </div>
    )

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

    return (
      <div className='row'>
        <div className='medium-1 columns'>&nbsp;</div>
          <div className='medium-10 columns'>
            <div>
              {docForm}
            </div>
            <div className='medium-12 columns'>
              {review_table}
            </div>
          </div>
        <div className='medium-1 columns'>&nbsp;</div>
      </div>
    )
  }
})

export default SourceDataContainer
