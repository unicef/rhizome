import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import LocationDetail from 'components/organisms/locations/LocationDetail'
import { updateLocation, getAllLocationTypes } from 'actions/location_actions'

const mapStateToProps = (state, ownProps) => {
	return {
		location: state.locations.raw ? state.locations.index[ownProps.params.location_id] : [],
		locations: state.locations,
		location_types: state.location_types
	}
}

const mapDispatchToProps = dispatch => bindActionCreators({
		getAllLocationTypes,
		updateLocation
	}
, dispatch)

const LocationContainer = connect(mapStateToProps, mapDispatchToProps)(LocationDetail)

export default LocationContainer
