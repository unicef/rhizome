import _ from 'lodash'
import React from 'react'

import SubmissionModal from 'components/organisms/source-data/SubmissionModal'
import MapForm from 'components/organisms/source-data/MapForm'

import Datascope from 'components/organisms/datascope/Datascope'
import LocalDatascope from 'components/organisms/datascope/LocalDatascope'

import parseSchema from 'components/organisms/manage-system/utils/parseSchema'

var ReviewTable = React.createClass({
  propTypes: {
    title: React.PropTypes.string.isRequired,
    getData: React.PropTypes.func.isRequired,
    fields: React.PropTypes.array.isRequired,
    header: React.PropTypes.array.isRequired,
    loading: React.PropTypes.bool.isRequired,
    location: React.PropTypes.object.isRequired,
    campaign: React.PropTypes.object.isRequired,
    doc_tab: React.PropTypes.string.isRequired,
    doc_id: React.PropTypes.number,
    datascopeFilters: React.PropTypes.string,
    children: React.PropTypes.array
  },

  getInitialState: function () {
    return {
      data: null,
      schema: null,
      query: {},
      loading: false,
      dashboardStore: {}
    }
  },

  getDefaultProps: function () {
    return {
      loading: false
    }
  },

  _callApi: function () {
    this.props.getData({
      document_id: this.props.doc_id
    }, null, {'cache-control': 'no-cache'})
    .then(response => {
      this.setState({
        schema: parseSchema(this.props.fields),
        data: response.objects
      })
    })
  },

  componentWillMount: function () {
    this._callApi()
  },

  componentWillUpdate: function (nextProps, nextState) {
    // FIXME -> needs cleanup
    if (nextProps.getData !== this.props.getData) {
      return
    }
    if (nextProps.doc_id !== this.props.doc_id) {
      return
    }
  },

  render () {

    const fields = {
      edit_link: {
        title: 'Edit',
        key: 'id',
        renderer: (id) => {
          if (this.props.doc_tab === 'viewraw') {
            return <SubmissionModal
              source_submission_id={id}
              key={id}/>
          } else if (this.props.doc_tab === 'doc_index') {
            return <a href={'/source-data/viewraw/' + id}>View Raw Data</a>
          } else if (this.props.doc_tab === 'un-mapped' || this.props.doc_tab === 'mapped') {
            return <MapForm
              source_object_map_id={id}
              onModalClose={this._callApi}/>
          }
        }
      }
    }

    var isLoaded = _.isArray(this.state.data) && this.state.schema && (!this.state.loading)
    if (!isLoaded) return this.renderLoading()

    var {data, schema} = this.state

    return (
      <div>
      <LocalDatascope
        data={data}
        schema={schema}
        fields={fields}
        pageSize={25}>
        <Datascope>
          {this.props.datascopeFilters ? this.renderFilters() : null}
          {this.props.children}
        </Datascope>
      </LocalDatascope>
      </div>
    )
  },
  renderLoading () {
    return <div className='admin-loading'> Review Page Loading...</div>
  },

  onToggleFilterContainer () {
    this.setState(prevState => ({ areFiltersVisible: !prevState.areFiltersVisible }))
  },

  renderFilters () {
    var recent = this.props.doc_tab === 'doc_index' ? (<div>
      <div className='upload__csv--load'>recent uploaded data</div>
      <div className='upload__csv--step'>You may review the recent uploaded data.</div>
    </div>) : null

    return (
      <div className='row'>
        <div className='large-7 medium-9 small-12 columns'>
          {recent}
        </div>
        <div className='large-5 medium-3 small-12 columns columns upload__csv--search'>
          <div className='ufadmin-filters-content'>
            {this.props.datascopeFilters}
          </div>
        </div>
      </div>
    )
  }
})

export default ReviewTable
