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

var SubmissionModal = React.createClass({
	propTypes: {
	  source_submission_id 	: React.PropTypes.number.isRequired,
    },

	getInitialState: function() {
		return {
				modalIsOpen: false,
			 	source_submission_id: null
			}
	},

  openModal: function() {
    this.setState({ modalIsOpen: true });
		console.log('call the api and get the image data..')

    api.submission({id: this.props.source_submission_id})
		.then(response => this.setState({
				img_location: response.objects[0].img_location,
		}));
  },

  closeModal: function() {
    this.setState({modalIsOpen: false});
  },


render : function(){

  var source_submission_id = this.props.source_submission_id
  var modalStyle = {width:650, height:500, marginLeft:400};

  return <div>
						<button
							className="tiny"
							onClick={this.openModal}
						> view raw data!
						</button>
	          <Modal
	            style={modalStyle}
	            isOpen={this.state.modalIsOpen}
	            onRequestClose={this.closeModal}
	          >
	              <h1> Source_submission_id: {source_submission_id} </h1>

								<img src={this.state.img_location} />

	          </Modal>
					</div>

},
});

module.exports = SubmissionModal;
