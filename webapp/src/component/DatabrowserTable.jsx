import React from 'react'
import parseSchema from 'ufadmin/utils/parseSchema'

// const {
//   Datascope, LocalDatascope
// } = require('react-datascope')

let DatabrowserTable = React.createClass({
  propTypes: {
    getData: React.PropTypes.func.isRequired,
    fields: React.PropTypes.array.isRequired,
    options: React.PropTypes.string.isRequired,
    children: React.PropTypes.array
  },

  getInitialState: function () {
    return {
      data: null,
      schema: null
    }
  },

  _callApi: function () {
    this.props.getData(this.props.options, null, {'cache-control': 'no-cache'})
      .then(response => {
        this.setState({
          data: response.objects,
          schema: parseSchema(this.props.fields)
        })
      })
  },

  componentWillMount: function () {
    this._callApi()
  },

  componentWillUpdate: function (nextProps, nextState) {
    if (nextProps.fields !== this.props.fields) {
      this._callApi()
      return
    }
  },

  render: function () {
    return (
      <div>
        table
      </div>
    )
  }
})

export default DatabrowserTable
