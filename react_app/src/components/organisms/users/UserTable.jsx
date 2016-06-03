import _ from 'lodash'
import React, { PropTypes, Component } from 'react'
import ResourceTable from 'components/molecules/ResourceTable'

class UserTable extends Component {
  static propTypes = {
    fetchUsers: PropTypes.func,
    users: PropTypes.objectOf(PropTypes.shape({
      id: PropTypes.number.isRequired,
      username: PropTypes.string.isRequired,
      first_name: PropTypes.string,
      last_name: PropTypes.string,
      email: PropTypes.string,
      is_staff: PropTypes.boolean,
      is_active: PropTypes.boolean,
      date_joined: PropTypes.string
    }).isRequired)
  }

  columnDefs = [
    {headerName: "ID", field: "id"},
    {headerName: "Username", field: "username"},
    {headerName: 'First_name', field: 'first_name', hide: true},
    {headerName: 'Last_name', field: 'last_name', hide: true},
    {headerName: 'Email', field: 'email', hide: true},
    {headerName: 'Is_staff', field: 'is_staff', hide: true},
    {headerName: 'Is_active', field: 'is_active', hide: true},
    {headerName: 'Date_joined', field: 'date_joined', hide: true}
  ]

  componentWillMount() {
    this.props.fetchUsers()
  }

  render = () => {
    return (
      <ResourceTable
        rowData={_.toArray(this.props.users)}
        onRefreshData={this.props.fetchUsers}
        columnDefs={this.columnDefs}
        resourcePath='users' />
    )
  }
}

export default UserTable
