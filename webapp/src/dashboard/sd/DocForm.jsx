var _ = require('lodash')
var React = require('react')
var Reflux = require('reflux')

var TitleMenu = require('component/TitleMenu.jsx')
var MenuItem = require('component/MenuItem.jsx')
var FileInput = require('react-file-input')
var Dropzone = require('react-dropzone')

var DocFormActions = require('actions/DocFormActions')
var DocFormStore = require('stores/DocFormStore')

var DocForm = React.createClass({
    // see here: https:// fitacular.com/blog/react/2014/06/23/react-file-upload-base64/

    mixins: [
        Reflux.connect(DocFormStore)
    ],

    // since we are starting off without any data, there is no initial value
    getInitialState: function () {
        return {
            data_uri: null,
            config_options: [],
            uq_id_column: null,
            location_column: null,
            campaign_column: null,
            created_doc_id: null,
            doc_detail_meta: null,
            doc_is_refreshed: false,
            new_doc_title: null
        }
    },

    onDrop: function (files) {
        this.handleFile(files[0])
    },

    // prevent form from submitting; we are going to capture the file contents
    handleSubmit: function (e) {
        e.preventDefault()
    },

    // when a file is passed to the input field, retrieve the contents as a
    // base64-encoded data URI and save it to the component's state
    handleFile: function (file) {
        var self = this

        var reader = new FileReader()

        reader.onload = function (upload) {
            DocFormActions.getData(file, upload)
        }
        reader.readAsDataURL(file)
    },

    setDocConfig: function (config_type, config_val) {
        var self = this
        var doc_detail_type_lookup = {}

        var doc_detail_meta = self.state.doc_detail_meta
        var doc_detail_type = doc_detail_meta[config_type]
        var doc_detail_type_id = doc_detail_type['id']

        // console.log('doc_detail_type',doc_detail_type['id'])
        // console.log('doc_detail_type_id',doc_detail_type_id)

        DocFormActions.setDocConfig({
            document_id: self.state.created_doc_id,
            doc_detail_type_id: doc_detail_type_id,
            doc_detail_value: config_val
        }, config_type)
    },

    syncDocData: function (config_val) {
        var self = this
        DocFormActions.transformUpload({document_id: self.state.created_doc_id})
    },

    buildHeaderList: function (config_type) {
        var state_header = this.state.config_options

        return MenuItem.fromArray(
            _.map(state_header, d => {
                return {
                    title: d.replace('"', ''),
                    value: d.replace('"', '')
                }
            }),
            this.setDocConfig.bind('config_type', config_type))
    },

    // return the structure to display and bind the onChange, onSubmit handlers
    render: function () {
        var uqHeaderList = this.buildHeaderList('uq_id_column')
        var rgHeaderList = this.buildHeaderList('location_column')
        var cpHeaderList = this.buildHeaderList('campaign_column')

        var fileConfigForm
        if (this.state.created_doc_id) {
            var uq_col = this.state.uq_id_column
            // var uq_col = this.state.data['']
            var rg_col = this.state.location_column
            var cp_col = this.state.campaign_column

            fileConfigForm = <div>
                <ul>
                    <li>
                        Unique ID Column:
                        <TitleMenu text={uq_col}>
                            {uqHeaderList}
                        </TitleMenu>
                    </li>
                    <li>
                        location Column:
                        <TitleMenu text={rg_col}>
                            {rgHeaderList}
                        </TitleMenu>
                    </li>
                    <li>
                        Campaign Column:
                        <TitleMenu text={cp_col}>
                            {cpHeaderList}
                        </TitleMenu>
                    </li>
                </ul>
            </div>
        } else {
            fileConfigForm = ''
        }

        var refreshBtn
        if (this.state.uq_id_column && this.state.location_column && this.state.campaign_column) {
            refreshBtn = <button onClick={this.syncDocData}> Sync Data</button>
        } else {
            refreshBtn = ''
        }

        var reviewBtn
        if (this.state.uq_id_column && this.state.location_column && this.state.campaign_column && this.state.doc_is_refreshed) {
            var next_link = '/datapoints/source-data/Nigeria/2015/06/viewraw/' + this.state.created_doc_id
            // FIXME ^^
            reviewBtn = <a href={next_link} className='button'> Review Upload</a>
        } else {
            reviewBtn = ''
        }

        var divZoneStyle = {
            margin: 'auto',
            width: '50%',
            padding: '10px',
            border: '2px dashed #0087F7'
        }

        var dropZoneStyle = {
            minHeight: '100px',
            padding: '54px 54px',
            marginRight: '150px'
        }

        // since JSX is case sensitive, be sure to use 'encType'
        return (<div style={divZoneStyle}>
            <Dropzone onDrop={this.onDrop} style={dropZoneStyle}>
                <div style={{textAlign: 'center'}}>Click here, or Drag a File to Upload New Data!</div>
            </Dropzone>
            {fileConfigForm}
            {refreshBtn}
            {reviewBtn}
        </div>)
    }
})

module.exports = DocForm
