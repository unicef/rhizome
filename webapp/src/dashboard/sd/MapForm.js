var _ = require('lodash');
var React = require('react');
var api = require('data/api');
var RegionTitleMenu     = require('component/RegionTitleMenu.jsx');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');
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
		source_object_code		: React.PropTypes.string.isRequired,
    regions : React.PropTypes.object.isRequired,
    campaigns : React.PropTypes.object.isRequired,
    indicators : React.PropTypes.object.isRequired,
    },

	getInitialState: function() {
		return { modalIsOpen: false, master_object_id: null }
	},

  openModal: function() {
    this.setState({ modalIsOpen: true });

    api.get_source_object_map({id: this.props.source_object_map_id})
		.then(response => this.setState({
				source_object_code: response.objects[0].source_object_code,
				content_type: response.objects[0].content_type,
		}));
  },

  closeModal: function() {
    this.setState({modalIsOpen: false, content_type: null});
  },

  postMetaMap : function(master_object_id) {
		console.log('logging post meta map')
		console.log('logging post meta map')
		console.log('logging post meta map')

    api.post_source_object_map({
        id: this.props.source_object_map_id,
        source_object_code: this.state.source_object_code,
        content_type: this.state.content_type,
        master_object_id: master_object_id,
        mapped_by_id: 1 // FIXME
      }).then(response => this.setState({
				master_object_id: response.objects.updated_values.master_object_id
		}));

  },

  renderDropDown : function(content_type) {
    var defaultSelected = {'name':'please map..'}

    if (content_type == 'region') {
      return <div><RegionTitleMenu
               regions={this.props.regions}
               selected={defaultSelected}
               sendValue={this.postMetaMap} /></div>;
    }
    if (content_type == 'indicator') {
      return <div>
        <IndicatorDropdownMenu
        text='Map Indicator'
        indicators={this.props.indicators.objects}
        sendValue={this.postMetaMap}>
      </IndicatorDropdownMenu></div>;
    }
    if (content_type == 'campaign') {
      return <div>
      <CampaignDropdownMenu
        text={defaultSelected}
        campaigns={this.props.campaigns}
        sendValue={this.postMetaMap}>
      </CampaignDropdownMenu>
      </div>;
     }
  },


render : function(){

  var source_object_map_id = this.props.source_object_map_id
  var modalStyle = {width:400, height:300, marginLeft:400};

  return <div><button className="tiny" onClick={this.openModal}> map! </button>
          <Modal
            style={modalStyle}
            isOpen={this.state.modalIsOpen}
            onRequestClose={this.closeModal}
          >
              <h1> Source Map Id: {source_object_map_id} </h1>
              <form>
              <h2> Content Type: {this.state.content_type} </h2>
              <h2> Source Code: {this.state.source_object_code} </h2>
              <h2> Master Object ID : {this.state.master_object_id} </h2>
              <h2> {this.renderDropDown(this.state.content_type)} </h2>
              </form>
          </Modal></div>

},
});

module.exports = MapForm;
