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
		modalForm : React.PropTypes.object,
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
  },

  closeModal: function() {
    this.setState({modalIsOpen: false});
  },


	render : function(){

  var modalStyle = {'margin':'auto','marginTop':'50px', 'width':'50%', 'height':'300px'};
	var contentType = this.props.contentType;
	var modalForm = this.props.modalForm;

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
	              <h1> {contentType} </h1>
								{modalForm}
	          </Modal>
					</div>

		},
});

module.exports = SimpleFormModal;
