import React from 'react'
import Reflux from 'reflux'

import DataBrowserTableStore from 'stores/DataBrowserTableStore'
import DataBrowserTableActions from 'actions/DataBrowserTableActions'
import SimpleDataTable from 'components/organisms/SimpleDataTable'

const {Datascope, LocalDatascope, SimpleDataTableColumn, Paginator} = require('react-datascope')

let DatabrowserTable = React.createClass({

  mixins: [
    Reflux.connect(DataBrowserTableStore)
  ],

  propTypes: {
    data: React.PropTypes.object.isRequired,
    editable: React.PropTypes.bool,
    selected_locations: React.PropTypes.array.isRequired,
    selected_indicators: React.PropTypes.array.isRequired
  },

  componentWillReceiveProps: function (nextProps) {
    if (nextProps.data) {
      DataBrowserTableActions.getTableData(nextProps.selected_locations, nextProps.selected_indicators, nextProps.data)
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    let shouldUpdate = nextState !== this.state
    return shouldUpdate
  },

  render: function () {
    if (!this.state || !this.state.data) {
      return (<div className='medium-12 columns ds-data-table-empty'>No data.</div>)
    } else {
      let columns = this.state.columns.map(column => (<SimpleDataTableColumn name={column}/>))
      let table = ''
      if (this.props.editable) {
        table = <SimpleDataTable editable>{columns}</SimpleDataTable>
      } else {
        table = <SimpleDataTable>{columns}</SimpleDataTable>
      }

      return (
        <LocalDatascope data={this.state.data} schema={this.state.schema} pageSize={10}>
          <Datascope>
            { table }
            <Paginator />
          </Datascope>
        </LocalDatascope>
      )
    }
  }
})

export default DatabrowserTable
