var _ = require('lodash')
var React = require('react')
const {
  Datascope, LocalDatascope,
  ClearQueryLink
  } = require('react-datascope')

var parseSchema = require('./utils/parseSchema')

var AdminPage = React.createClass({
  propTypes: {
    title: React.PropTypes.string.isRequired,
    getData: React.PropTypes.func.isRequired,
    schema: React.PropTypes.object,
    fields: React.PropTypes.object,
    datascopeFilters: React.PropTypes.element,
    children: React.PropTypes.array
  },
  getInitialState: function () {
    return {
      data: null,
      schema: null,
      query: {},
      areFiltersVisible: true
    }
  },

  componentWillMount: function () {
    this.props.getData(null, null, {'cache-control': 'no-cache'}).then(response => {
      var schema = parseSchema(response)
      if (this.props.schema !== null) {
        var schemaSetting = this.props.schema
        _.each(schemaSetting, function (item, key) {
          schema.items.properties[key].type = item.type
          schema.items.properties[key].format = item.format
        })
      }
      this.setState({
        schema: schema,
        data: response.objects
      })
    })
  },

  onToggleFilterContainer () {
    this.setState(prevState => ({ areFiltersVisible: !prevState.areFiltersVisible }))
  },

  render () {
    // render loading indicator until data has loaded
    var isLoaded = _.isArray(this.state.data) && this.state.schema
    if (!isLoaded) return this.renderLoading()

    var {data, schema} = this.state

    // make the 'Create X' button if we have a creation URL
    var createUrl = '/datapoints/users/create/'
    if (this.props.title === 'Campaigns') createUrl = '/datapoints/campaigns/create/'
    if (this.props.title === 'locations') createUrl = '/datapoints/locations/create/'
    else if (this.props.title === 'Indicators') createUrl = '/ufadmin/manage/indicator/'
    else if (this.props.title === 'Tags') createUrl = '/ufadmin/manage/indicator_tag/'

    // strip the 's' from the end of plural title
    var titleSingular = _.endsWith(this.props.title, 's') ? _.initial(this.props.title).join('') : this.props.title
    var createButton = createUrl
      ? <div className='ufadmin-create-button'>
          <a className='button' href={createUrl}>Create {titleSingular}</a>
        </div>
      : null

    return <div>
      <h2 className='ufadmin-page-heading'>{this.props.title} Admin Page</h2>

      {createButton}

      <LocalDatascope data={data} schema={schema} fields={this.props.fields} pageSize={100}>
        <Datascope>

          {this.props.datascopeFilters ? this.renderFilters() : null}

          {this.props.children}

        </Datascope>
      </LocalDatascope>
    </div>
  },

  renderLoading () {
    return <div className='admin-loading'>Loading...</div>
  },

  renderOriginalFilters () {
    var filterExpander = this.state.areFiltersVisible ? '[-]' : '[+]'
    var { areFiltersVisible } = this.state

    return <div className='ufadmin-filters-container'>
      <div className='ufadmin-show-filters' onClick={this.onToggleFilterContainer}>

        {areFiltersVisible
          ? <span>
              <ClearQueryLink>
                Filter results {filterExpander}
              </ClearQueryLink>
              <span onClick={e => { e.stopPropagation() }}>
                <ClearQueryLink>
                  <a className='admin-clear-filters'>Clear filters</a>
                </ClearQueryLink>
              </span>
            </span>
          : <span>Filter results {filterExpander}</span>
        }
      </div>

      {areFiltersVisible
        ? <div className='ufadmin-filters-content'>
            {this.props.datascopeFilters}
          </div>
        : null
      }
    </div>
  },

  renderFilters () {
    var { areFiltersVisible } = this.state
    return areFiltersVisible
      ? <div className='row'>
          <div className='medium-7 columns'>
          </div>
          <div className='medium-5 columns'>
            <div className='ufadmin-filters-content'>
              {this.props.datascopeFilters}
            </div>
          </div>
        </div>
      : null
  }
})

module.exports = AdminPage
