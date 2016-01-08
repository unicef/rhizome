import React from 'react'
import Reflux from 'reflux'

import UserGroupStore from 'stores/UserGroupStore'
import UserGroupActions from 'actions/UserGroupActions'

import GroupSelect from 'component/GroupSelect.jsx'

let UserGroup = React.createClass({
  mixins: [Reflux.connect(UserGroupStore)],

  propTypes: {
    userId: React.PropTypes.number
  },

  componentWillMount: function () {
    UserGroupActions.getUserGroupByUserId(this.props.userId)
  },

  render: function () {
    let groups = this.state.userGroups.map(userGroup => {
      return (
        <li>
          <GroupSelect
            data={userGroup}
            userId={this.props.userId}/>
        </li>
      )
    })
    return (
      <div className='columns small-8 right-box'>
        <ul className='user-roles'>
          {groups}
        </ul>
      </div>
    )
  }
})

export default UserGroup
