/**
 * Created by sczhang on 10/13/15.
 */
var React = require('react');
var _ = require('lodash');
var api = require('data/api');
var DropdownMenu = require('component/DropdownMenu.jsx');
var NavigationStore = require('stores/NavigationStore');

var DocOverview = React.createClass({
    propTypes: {
        doc_id: React.PropTypes.number.isRequired,
        doc_tab: React.PropTypes.string.isRequired,
        loading: React.PropTypes.bool
    },

    getDefaultProps: function () {
        return {
            loading: false
        };
    },

    getInitialState: function () {
        return {
            doc_id: null,
            doc_title: null,
            doc_detail_types: null,
            doc_deets: null,
        };
    },

    componentWillMount: function (nextProps, nextState) {
        this.pullDocDetailTypes()
        this.refreshMaster()
    },

    componentWillUpdate: function (nextProps, nextState) {
        if (nextProps.doc_id != this.props.doc_id) {
            return;
        }
        if (nextProps.doc_deets != this.props.doc_deets) {
            return;
        }
    },

    pullDocDetailTypes: function () {

        // api.docDetail({document_id: this.props.doc_id},null,{'cache-control':'no-cache'})
        // .then(response => this.setState({
        // 	doc_deets: response.objects,
        // }));

        api.docDetailType()
            .then(response => this.setState({
                doc_detail_types: response.objects,
            }));

    },

    refreshMaster: function () {

        api.refresh_master({document_id: this.props.doc_id}, null, {'cache-control': 'no-cache'})
            .then(response => this.setState({
                doc_deets: response.objects
            }));
    },

    renderLoading() {
        return <div className='admin-loading'> Doc Details Loading...</div>
    },

    render() {
        var doc_id = this.props.doc_id;
        var doc_tab = this.props.doc_tab;
        var doc_deets = this.state.doc_deets;

        if (!doc_deets) return this.renderLoading();

        var refresh_master_btn = <div>
            <button className="tiny" onClick={this.refreshMaster}> Refresh Master!
            </button>
        </div>

        var doc_detail_type_lookup = _.indexBy(this.state.doc_detail_types, 'id');

        var rows = [];
        for (var i = 0; i < doc_deets.length; i++) {
            var doc_detail = doc_deets[i]
            rows.push(<li>{doc_detail_type_lookup[doc_detail.doc_detail_type_id].name}
                : {doc_detail.doc_detail_value} </li>)
        }

        return <div>

            <h3> Document Overview </h3>
            <ul>{rows}</ul>
            {refresh_master_btn}
        </div>
    }
});

module.exports = DocOverview;
