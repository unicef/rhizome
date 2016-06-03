import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import LocationTable from 'components/organisms/locations/LocationTable'
import { fetchLocations } from 'actions/location_actions'

const mapStateToProps = (state) => ({ locations: state.locations })

const mapDispatchToProps = (dispatch) => bindActionCreators({fetchLocations}, dispatch)

const LocationTableContainer = connect(mapStateToProps, mapDispatchToProps)(LocationTable)

export default LocationTableContainer
