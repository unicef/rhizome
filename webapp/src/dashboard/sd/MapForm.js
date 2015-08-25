var _ = require('lodash');
var React = require('react');
var api = require('data/api');
var RegionTitleMenu     = require('component/RegionTitleMenu.jsx');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');
var DashboardStore    	= require('stores/DashboardStore');
var Modal = require('react-modal');

var appElement = document.getElementById('main');
Modal.setAppElement(appElement);
Modal.injectCSS();

const {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	ClearQueryLink,
	Paginator,
	SearchBar,
	FilterPanel, FilterDateRange, FilterInputRadio
	} = require('react-datascope');


var MapForm = React.createClass({
	propTypes: {
	  source_object_map_id 	: React.PropTypes.number.isRequired,
    },

	getInitialState: function() {
		return { modalIsOpen: false }
	},

  openModal: function() {
    console.log('opening modal..')
    this.setState({ modalIsOpen: true });

    api.get_source_object_map({id: this.props.source_object_map_id})
		.then(response => this.setState({
				response_data: response
		}));
    console.log(this.state)

  },

  closeModal: function() {
    this.setState({modalIsOpen: false});

  },

// postMetaMap : function(source_object_map_id) {
//   console.log('posting')
//   console.log(source_object_map_id)
// },

render : function(){
  console.log('rendering')
  var source_object_map_id = this.props.source_object_map_id

  // var source_object_name = source_object_map_id
  var content_type = 'region'

  // var dropDown = <RegionTitleMenu
  //                        regions={DashboardStore.regions}
  //                        selected={this.props.region}
  //                        sendValue={this.postMetaMap} />

  var modalStyle = {width:400, height:300, marginLeft:400}; // rendered as "height:10px"

  return <div><button className="tiny" onClick={this.openModal}> map! </button>
          <Modal
            style={modalStyle}
            isOpen={this.state.modalIsOpen}
            onRequestClose={this.closeModal}
          >
              <h2>Mapping for - {source_object_map_id} </h2>
              <form>
              {this.state.response_data}
              </form>
          </Modal></div>

},
});

module.exports = MapForm;
