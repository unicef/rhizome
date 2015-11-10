var _ = require('lodash')
var React = require('react')
var DashboardStore = require('stores/DashboardStore')

var SubmissionModal = require('dashboard/sd/SubmissionModal.jsx')
var MapForm = require('dashboard/sd/MapForm.jsx')
var api = require('data/api.js')

const {
  Datascope, LocalDatascope,
  SimpleDataTable, SimpleDataTableColumn,
  ClearQueryLink,
  Paginator,
  SearchBar,
  FilterPanel, FilterDateRange, FilterInputRadio
  } = require('react-datascope')

var parseSchema = require('ufadmin/utils/parseSchema')

var ReviewTable = React.createClass({
  propTypes: {
    title: React.PropTypes.string.isRequired,
    getData: React.PropTypes.func.isRequired,
    fields: React.PropTypes.array.isRequired,
    loading: React.PropTypes.bool.isRequired,
    location: React.PropTypes.object.isRequired,
    campaign: React.PropTypes.object.isRequired,
    doc_tab: React.PropTypes.string.isRequired
  },

  getInitialState: function () {
    return {
      data: null,
      schema: null,
      query: {},
      loading: false
    }
  },

  getDefaultProps: function () {
    return {
      loading: false
    }
  },

  validateForm: function (id) {
    // onclick post to api //
    return <input type='checkbox' checked/>
  },

  _callApi: function () {
    this.props.getData({
      document_id: this.props.doc_id,
      location_id: this.props.location.id,
      campaign_id: this.props.campaign.id
    }, null, {'cache-control': 'no-cache'})
    .then(response => {
      this.setState({
        schema: parseSchema(this.props.fields),
        data: response.objects
      })
    })
  },

  componentWillMount: function () {
    api.indicatorsTree().then(indicators => {
      this.setState({
        indicators: indicators.objects
      })

      this._callApi()
    })
  },

  componentWillReceiveProps: function (nextProps) {},

  componentWillUpdate: function (nextProps, nextState) {
    // FIXME -> needs cleanup
    if (nextProps.location !== this.props.location) {
      return
    }
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
          if (this.props.doc_tab === 'validate') {
            return this.validateForm(id)
          } else if (this.props.doc_tab === 'viewraw') {
            return <SubmissionModal
              source_submission_id={id}
              key={id}
              />
          } else if (this.props.doc_tab === 'doc_index') {
            return <a href={`/datapoints/source-data/Nigeria/2015/06/viewraw/${id}`}>View Raw Data</a>
          } else if (this.props.doc_tab === 'mapping') {
            return <MapForm
              indicators={this.state.indicators}
              campaigns={DashboardStore.campaigns}
              locations={DashboardStore.locations}
              source_object_map_id={id}
              key={id}
              onModalClose={this._callApi}
              />
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
    var filterExpander = this.state.areFiltersVisible ? '[-]' : '[+]'
    var { areFiltersVisible } = this.state

    return (
      <div className='row'>
      <div className='medium-7 columns'>
      </div>
      <div className='medium-5 columns'>
        <div className='ufadmin-filters-content'>
          {this.props.datascopeFilters}
        </div>
      </div>
      </div>
    )
  }
})

module.exports = ReviewTable
