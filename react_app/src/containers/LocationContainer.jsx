import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import LocationDetail from 'components/organisms/locations/LocationDetail'
import { updateLocation } from 'actions/location_actions'

const mapStateToProps = (state, ownProps) => {
	return {
		location: state.locations.raw ? state.locations.index[ownProps.params.location_id] : [],
		real_location: state.location,
		locations: state.locations
	}
}

const mapDispatchToProps = dispatch => bindActionCreators({	updateLocation }, dispatch)

const LocationContainer = connect(mapStateToProps, mapDispatchToProps)(LocationDetail)

export default LocationContainer
