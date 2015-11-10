var _ = require('lodash')
var moment = require('moment')
var React = require('react')
var Reflux = require('reflux')

var RegionTitleMenu = require('component/RegionTitleMenu')
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx')
var CampaignDropdownMenu = require('component/CampaignDropdownMenu.jsx')

var MapFormStore = require('stores/MapFormStore')
var Modal = require('react-modal')

var appElement = document.getElementById('main')

Modal.setAppElement(appElement)
Modal.injectCSS()

const {
    Datascope, LocalDatascope,
    SimpleDataTable, SimpleDataTableColumn,
    ClearQueryLink,
    Paginator,
    SearchBar,
    FilterPanel, FilterDateRange, FilterInputRadio
    } = require('react-datascope')

var MapForm = React.createClass({
    propTypes: {
        source_object_map_id: React.PropTypes.number.isRequired,
        source_object_code: React.PropTypes.string.isRequired,
        locations: React.PropTypes.object.isRequired,
        campaigns: React.PropTypes.object.isRequired,
        indicators: React.PropTypes.object.isRequired
    },

    getInitialState: function () {
        return {modalIsOpen: false, master_object_id: null}
    },

    openModal: function () {
        var self = this
        MapFormStore.getSourceMap({id: this.props.source_object_map_id}).then(function (data) {
            self.setState(
                {
                    source_object_code: data.source_object_code,
                    content_type: data.content_type,
                    master_object_id: data.master_object_id,
                    modalIsOpen: true
                })
        })
    },

    closeModal: function () {
        this.props.onModalClose()
        this.setState({modalIsOpen: false, content_type: null})
    },

    postMetaMap: function (masterObjectId) {
        var self = this
        MapFormStore.updateMetaMap({
            id: this.props.source_object_map_id,
            master_object_id: masterObjectId,
            mapped_by_id: 1 // FIXME
        }).then(function (data) {
            self.setState({master_object_id: data})
        })
    },

    renderDropDown: function (content_type) {
        var defaultSelected = {'name': 'please map..'}
        if (content_type === 'location') {
            return <div><RegionTitleMenu
                locations={this.props.locations}
                selected={defaultSelected}
                sendValue={this.postMetaMap}/></div>
        }
        if (content_type === 'indicator') {
            return <div>
                <IndicatorDropdownMenu
                    text='Map Indicator'
                    indicators={this.props.indicators}
                    sendValue={this.postMetaMap}>
                </IndicatorDropdownMenu></div>
        }
        if (content_type === 'campaign') {
          var office = {
            1: 'Nigeria',
            2: 'Afghanistan',
            3: 'Pakistan'
          }
          var campaigns = this.props.campaigns.map(campaign => {
            return _.assign({}, campaign, {
              slug: office[campaign.office_id] + ' ' + moment(campaign.start_date).format('MMM YYYY')
            })
          })
          return <div>
              <CampaignDropdownMenu
                  text={defaultSelected}
                  campaigns={campaigns}
                  sendValue={this.postMetaMap}>
              </CampaignDropdownMenu>
          </div>
        }
    },

    render: function () {
        var sourceObjectMapId = this.props.source_object_map_id
        var modalStyle = {width: 400, height: 300, marginLeft: 400}
        return <div>
            <button className='tiny' onClick={this.openModal}> map!</button>
            <Modal
                style={modalStyle}
                isOpen={this.state.modalIsOpen}
                onRequestClose={this.closeModal}
                >
                <h1> Source Map Id: {sourceObjectMapId} </h1>

                <form>
                    <h2> Content Type: {this.state.content_type} </h2>
                    <h2> Source Code: {this.state.source_object_code} </h2>
                    <h2> Master Object ID : {this.state.master_object_id} </h2>
                    {this.renderDropDown(this.state.content_type)}
                </form>
            </Modal></div>
    }
})

module.exports = MapForm
