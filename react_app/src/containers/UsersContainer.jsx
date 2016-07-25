import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import UserTable from 'components/organisms/users/UserTable'
import { getAllUsers } from 'actions/user_actions'

const mapStateToProps = (state) => ({ users: state.users })

const mapDispatchToProps = (dispatch) => bindActionCreators({getAllUsers}, dispatch)

const UsersContainer = connect(mapStateToProps, mapDispatchToProps)(UserTable)

export default UsersContainer
