import React from 'react'
import Reflux from 'reflux'

import DataBrowserTableStore from 'stores/DataBrowserTableStore'
import DataBrowserTableActions from 'actions/DataBrowserTableActions'

const { Datascope, LocalDatascope, SimpleDataTable, SimpleDataTableColumn, Paginator} = require('react-datascope')

let DatabrowserTable = React.createClass({

  mixins: [
    Reflux.connect(DataBrowserTableStore)
  ],

  propTypes: {
    data: React.PropTypes.object.isRequired
  },

  componentWillReceiveProps: function (nextProps) {
    let table_data = nextProps.data
    DataBrowserTableActions.getTableData(table_data.selected_locations, table_data.selected_indicators, table_data.data)
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
      return (
        <LocalDatascope data={this.state.data} schema={this.state.schema} pageSize={10}>
          <Datascope>
            <SimpleDataTable>{columns}</SimpleDataTable>
            <Paginator />
          </Datascope>
        </LocalDatascope>
      )
    }
  }
})

export default DatabrowserTable
