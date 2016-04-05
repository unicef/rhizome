import React from 'react'
import Reflux from 'reflux'

import DataBrowserTableStore from 'stores/DataBrowserTableStore'
import DataBrowserTableActions from 'actions/DataBrowserTableActions'
import SimpleDataTable from 'components/organisms/datascope/SimpleDataTable'

var { SimpleDataTableColumn, Paginator, LocalDatascope, Datascope } = require('react-datascope')

// import Datascope from 'components/organisms/datascope/Datascope'
// import SimpleDataTableColumn from 'components/organisms/datascope/SimpleDataTableColumn'
// import Paginator from 'components/organisms/datascope/Paginator'
// import LocalDatascope from 'components/organisms/datascope/SearchBar'

let DatabrowserTable = React.createClass({

  mixins: [
    Reflux.connect(DataBrowserTableStore)
  ],

  propTypes: {
    data: React.PropTypes.object,
    editable: React.PropTypes.bool,
    selected_locations: React.PropTypes.array.isRequired,
    selected_indicators: React.PropTypes.array.isRequired
  },

  render: function () {
    console.info('DataBrowserTable.jsx-------- DatabrowserTable.render')
    DataBrowserTableActions.getTableData(this.props.selected_locations, this.props.selected_indicators, this.props.data)
    if (!this.state || !this.props.data) {
      return (<div className='medium-12 columns ds-data-table-empty'>No data.</div>)
    } else {
      let columns = this.state.columns.map(column => (<SimpleDataTableColumn name={column}/>))
      console.log('columns:', columns)

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
