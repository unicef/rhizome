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
//
// 	getInitialState: function() {
// 		return {
// 			loading   : false,
//       source_object_map_id : null
//       doc_tab : null
// 		}
// 	},
//
// 	getDefaultProps : function () {
//     return {
//       loading : false
//     };
//   },
//
//
//
// openModal: function(source_object_map_id) {
//
//   this.setState({
//     modalIsOpen: true,
//     some_state_var: 'someeee-variable'
//   });
// },
//
// closeModal: function() {
//   this.setState({modalIsOpen: false});
// },
//
// postMetaMap : function(source_object_map_id) {
//   console.log('posting')
//   console.log(source_object_map_id)
// },

render : function(){

  return <div> yo </div>

  // var source_object_name = source_object_map_id
  // var content_type = 'region'
  // //
  // var dropDown = <RegionTitleMenu
  //                        regions={DashboardStore.regions}
  //                        selected={this.props.region}
  //                        sendValue={this.postMetaMap} />
  // //
  //
  // var modalStyle = {width:400, marginLeft:400}; // rendered as "height:10px"
  //
  // return <div><button className="tiny" onClick={this.openModal(source_object_map_id)}> map! </button>
  //         <Modal
  //           style={modalStyle}
  //           isOpen={this.state.modalIsOpen}
  //           onRequestClose={this.closeModal}
  //         >
  //             <h2>Mapping for {content_type} - {this.state.some_state_var} </h2>
  //             <form>
  //             {dropDown}
  //             </form>
  //         </Modal></div>

},
});

module.exports = MapForm;
