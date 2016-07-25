import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import LocationTable from 'components/organisms/locations/LocationTable'
import { getAllLocations } from 'actions/location_actions'

const mapStateToProps = (state) => ({ locations: state.locations })

const mapDispatchToProps = (dispatch) => bindActionCreators({getAllLocations}, dispatch)

const LocationsContainer = connect(mapStateToProps, mapDispatchToProps)(LocationTable)

export default LocationsContainer
