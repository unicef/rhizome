import _ from 'lodash'
import React, { PropTypes, Component } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'
import Placeholder from 'components/global/Placeholder'

class UserTable extends Component {
  componentWillMount() {
    this.props.getAllUsers()
  }

  render = () => {
    const columnDefs = [
      {headerName: "ID", field: "id"},
      {headerName: "Username", field: "username"},
      {headerName: 'First_name', field: 'first_name', hide: true},
      {headerName: 'Last_name', field: 'last_name', hide: true},
      {headerName: 'Email', field: 'email', hide: true},
      {headerName: 'Is_staff', field: 'is_staff', hide: true},
      {headerName: 'Is_active', field: 'is_active', hide: true},
      {headerName: 'Date_joined', field: 'date_joined', hide: true}
    ]

    return this.props.users.raw ? (
      <ResourceTable
        rowData={this.props.users.raw}
        onRefreshData={() => this.props.getAllUsers()}
        columnDefs={columnDefs}
        resourcePath='users' />
    ) : <Placeholder />
  }
}

export default UserTable
