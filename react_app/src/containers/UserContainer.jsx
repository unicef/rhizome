import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import UserDetail from 'components/organisms/users/UserDetail'
import { updateUser, getAllUsers } from 'actions/user_actions'

const mapStateToProps = (state, ownProps) => {
	return {
		user: state.users.raw ? state.users.index[ownProps.params.user_id] : [],
		users: state.users,
		locations: state.locations
	}
}

const mapDispatchToProps = dispatch => bindActionCreators({
	getAllUsers,
	updateUser
}, dispatch)

const UserContainer = connect(mapStateToProps, mapDispatchToProps)(UserDetail)

export default UserContainer
