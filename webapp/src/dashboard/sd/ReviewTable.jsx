var _ = require('lodash');
var React = require('react')
var Reflux = require('reflux');

var DashboardStore = require('stores/DashboardStore');
var GroupFormStore = require('stores/GroupFormStore');
var ChartBuilderStore = require('stores/ChartBuilderStore');

var SubmissionModal = require('dashboard/sd/SubmissionModal.js');
var MapForm = require('dashboard/sd/MapForm.jsx');
var ReviewTableActions = require('actions/ReviewTableActions');
var ReviewTableStore = require('stores/ReviewTableStore');

const {
    Datascope, LocalDatascope,
    SimpleDataTable, SimpleDataTableColumn,
    ClearQueryLink,
    Paginator,
    SearchBar,
    FilterPanel, FilterDateRange, FilterInputRadio
    } = require('react-datascope');

var ReviewTable = React.createClass({
    mixins: [
        Reflux.connect(ReviewTableStore)
    ],

    propTypes: {
        title: React.PropTypes.string.isRequired,
        fields: React.PropTypes.array.isRequired,
        loading: React.PropTypes.bool.isRequired,
        location: React.PropTypes.object.isRequired,
        campaign: React.PropTypes.object.isRequired,
        doc_tab: React.PropTypes.string.isRequired,
    },

    getInitialState: function () {
        return {
            data: null,
            schema: null,
            query: {},
            loading: false,
        }
    },

    getDefaultProps: function () {
        return {
            loading: false
        };
    },

    validateForm: function (id) {
        return <input type="checkbox" checked/>;
    },

    getData: function () {
        ReviewTableActions.getData({
            document_id: this.props.doc_id,
            location_id: this.props.location.id,
            campaign_id: this.props.campaign.id
        }, this.props.fields, this.props.doc_tab);
        this.forceUpdate();
    },

    componentWillMount: function () {
        ReviewTableActions.getIndicators();
        this.getData()
    },

    componentWillReceiveProps: function (nextProps) {
        this.getData()
    },

    componentWillUpdate: function (nextProps, nextState) {
        // FIXME -> needs cleanup
        if (nextProps.location != this.props.location) {
            return;
        }
        if (nextProps.getData != this.props.getData) {
            return;
        }
        if (nextProps.doc_id != this.props.doc_id) {
            return;
        }
    },


    render() {

        const fields = {
            edit_link: {
                title: 'Edit',
                key: 'id',
                renderer: (id) => {
                    if (this.props.doc_tab == 'validate') {
                        return this.validateForm(id)
                    }
                    else if (this.props.doc_tab == 'viewraw') {
                        return <SubmissionModal
                            source_submission_id={id}
                            key={id}
                            />
                    }
                    else if (this.props.doc_tab == 'doc_index') {
                        return <a href={`/datapoints/source-data/Nigeria/2015/06/viewraw/${id}`}>View Raw Data</a>;
                    }
                    else if (this.props.doc_tab == 'mapping') {
                        return <MapForm
                            indicators={this.state.indicators}
                            campaigns={DashboardStore.campaigns}
                            locations={DashboardStore.locations}
                            source_object_map_id={id}
                            key={id}
                            />
                    }
                }
            },
        };

        var isLoaded = _.isArray(this.state.data) && this.state.schema && (!this.state.loading);
        if (!isLoaded) return this.renderLoading();

        var {data, schema} = this.state;

        return <div>
            <LocalDatascope
                data={data}
                schema={schema}
                fields={fields}
                pageSize={25}>
                <Datascope>
                    {this.props.datascopeFilters ? this.renderFilters() : null}
                    {this.props.children}
                </Datascope>
            </LocalDatascope>
        </div>
    },
    renderLoading() {
        return <div className='admin-loading'> Review Page Loading...</div>
    },

    onToggleFilterContainer() {
        this.setState(prevState => ({areFiltersVisible: !prevState.areFiltersVisible}));
    },

    renderFilters() {
        var filterExpander = this.state.areFiltersVisible ? '[-]' : '[+]';
        var { areFiltersVisible } = this.state;

        return <div className="row">
            <div className="medium-7 columns">
            </div>
            <div className="medium-5 columns">
                <div className="ufadmin-filters-content">
                    {this.props.datascopeFilters}
                </div>
            </div>
        </div>
    }
});


module.exports = ReviewTable;
