import React from 'react'
import Reflux from 'reflux'

import DataBrowserTableStore from 'stores/DataBrowserTableStore'

const {
  Datascope, LocalDatascope
} = require('react-datascope')

let {
  SimpleDataTable, SimpleDataTableColumn,
  Paginator
} = require('react-datascope')

let DatabrowserTable = React.createClass({
  propTypes: {
    fields: React.PropTypes.array.isRequired,
    options: React.PropTypes.string.isRequired
  },

  mixins: [Reflux.connect(DataBrowserTableStore, 'data')],

  componentWillUpdate: function (nextProps, nextState) {
    return nextProps.fields !== this.props.fields
  },

  render: function () {
    console.log(this.state.data)
    if (this.state.data === null || this.state.data.data === null) {
      return (<div className='medium-12 columns ds-data-table-empty'>No data.</div>)
    } else {
      return (<LocalDatascope
          data={this.state.data.data}
          schema={this.state.data.schema}
          pageSize={10} >
          <Datascope>
            <SimpleDataTable>
              {this.state.data.fields.map(column => {
                return <SimpleDataTableColumn name={column}/>
              })}
            </SimpleDataTable>
            <Paginator />
          </Datascope>
        </LocalDatascope>)
    }
  }
})

export default DatabrowserTable
