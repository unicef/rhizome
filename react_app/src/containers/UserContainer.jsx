import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import UserDetail from 'components/organisms/users/UserDetail'
import { updateUser } from 'actions/user_actions'

const mapStateToProps = (state, ownProps) => {
	return {
		user: state.users.raw ? state.users.index[ownProps.params.user_id] : [],
		real_user: state.user,
		users: state.users
	}
}

const mapDispatchToProps = dispatch => bindActionCreators({	updateUser }, dispatch)

const UserContainer = connect(mapStateToProps, mapDispatchToProps)(UserDetail)

export default UserContainer
