var _ = require('lodash');
var React = require('react');
var api = require('data/api');
var RegionTitleMenu     = require('component/RegionTitleMenu');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx');
var Modal = require('react-modal');

var appElement = document.getElementById('main');
Modal.setAppElement(appElement);
Modal.injectCSS();

var SimpleFormModal = React.createClass({
	propTypes: {
	  onClick 	: React.PropTypes.isRequired,
		contentType : React.PropTypes.string.isRequired,

  },

	getInitialState: function() {
		return {
				modalIsOpen: false,
			}
	},

  openModal: function() {
    this.setState({ modalIsOpen: true });
    // api.submission({id: this.props.source_submission_id})
		// .then(response => this.setState({
		// 		submission_data: response.objects[0],
		// }));
  },

  closeModal: function() {
    this.setState({modalIsOpen: false});
  },


render : function(){

  var modalStyle = {width:650, height:500, marginLeft:400};
	var contentType = this.props.contentType;

  return <div>
						<span
							className="fa fa-plus fa-large"
							onClick={this.openModal}
						> Create New {contentType}!
						</span>
	          <Modal
	            style={modalStyle}
	            isOpen={this.state.modalIsOpen}
	            onRequestClose={this.closeModal}
	          >
	              <h1> SOMETHING </h1>
	          </Modal>
					</div>

		},
});

module.exports = SimpleFormModal;
