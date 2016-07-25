import _ from 'lodash'
import moment from 'moment'
import React, { Component, PropTypes } from 'react'
import {AgGridReact} from 'ag-grid-react';
import Placeholder from 'components/global/Placeholder'
import DateRangeSelect from 'components/select/DateRangeSelect'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import DropdownButton from 'components/button/DropdownButton'
import DropdownList from 'react-widgets/lib/DropdownList'
import IconButton from 'components/button/IconButton'
import Multiselect from 'react-widgets/lib/Multiselect'

class UserDetail extends Component {

  constructor (props) {
    super(props)
    this.state = {}
  }

  componentDidMount() {
    if (!this.props.users.raw) {
      this.props.getAllUsers()
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.user.id !== this.state.id) {
      const user = Object.assign({}, nextProps.user)
      delete user.created_at
      this.setState(user)
    }
  }

  _updateParam = (param, value) => {
    const user = {}
    user[param] = value
    this.setState(user)
  }

  _saveUser = event => {
    event.preventDefault()
    this.props.updateUser(this.state)
  }

  render = () => {
    if (!this.state.id) {
      return <Placeholder height={300} />
    }

    return (
      <form className='medium-5 medium-centered columns resource-form' onSubmit={this._saveUser}>
        <h2>User ID: {this.state.id}</h2>
        <label htmlFor='username'>Username:
          <input type='text' defaultValue={this.state.username}
            onBlur={event => this._updateParam('username', event.target.value)}
          />
        </label>
        <label htmlFor='first_name'>First Name:
          <input type='text' defaultValue={this.state.first_name}
            onBlur={event => this._updateParam('first_name', event.target.value)}
          />
        </label>
        <label htmlFor='last_name'>Last Name:
          <input type='text' defaultValue={this.state.last_name}
            onBlur={event => this._updateParam('last_name', event.target.value)}
          />
        </label>
        <label htmlFor='email'>Email:
          <input type='text' defaultValue={this.state.email}
            onBlur={e => this._updateParam('email', e.target.value)}
          />
        </label>
        <button className='large primary button expand'>Save</button>
      </form>
    )
  }
}

export default UserDetail
