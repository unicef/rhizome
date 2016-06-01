import React from 'react'
import Reflux from 'reflux'

import UserGroupStore from 'stores/UserGroupStore'
import UserGroupActions from 'actions/UserGroupActions'

let UserGroup = React.createClass({
  mixins: [Reflux.connect(UserGroupStore)],

  propTypes: {
    userId: React.PropTypes.number
  },

  componentWillMount: function () {
    UserGroupActions.getUserGroupByUserId(this.props.userId)
  },

  _changeSelect: function (actived, groupId) {
    UserGroupActions.changeSelectGroup(actived, this.props.userId, groupId)
  },

  render: function () {
    let groups = this.state.userGroups.map(userGroup => {
      let changeSelect = this._changeSelect.bind(this, userGroup.active, userGroup.id)
      return (
        <li>
          <input type='checkbox'
                 checked={userGroup.active}
                 onClick={changeSelect}>
            <span>{userGroup.name}</span>
          </input>
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
