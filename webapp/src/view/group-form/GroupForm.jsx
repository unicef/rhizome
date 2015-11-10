'use strict'

var React = require('react')
var Reflux = require('reflux')

var GroupFormStore = require('stores/GroupFormStore')
var GroupFormActions = require('actions/GroupFormActions')
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx')
var List = require('component/list/List.jsx')

module.exports = React.createClass({
    mixins: [ Reflux.connect(GroupFormStore, 'store') ],

    componentWillMount: function () {
        // init store, passing group id if present
        GroupFormActions.initialize(this.props.group_id)
    },

    updateName: function (e) {
        GroupFormActions.updateName(e.target.value)
    },

    submitForm: function (e) {
        GroupFormActions.saveGroupForm()
        e.preventDefault()
    },

    render: function () {
        var indicators = (<strong>This role cannot enter data for any indicators.</strong>)
        if (this.state.store.indicatorsSelected.length > 0) {
            indicators = (<div><strong>This role can enter data for the following indicators:</strong>
                              <List
                                items={this.state.store.indicatorsSelected}
                                removeItem={GroupFormActions.removeIndicatorSelection} />
                          </div>)
        }

        if (this.state.store.loading) {
            return (<div><i className='fa fa-spinner fa-spin'></i> Loading...</div>)
        }

        var indicatorsSection = ''
        if (!this.state.store.groupId) { // no id yet -- creating new
            indicatorsSection = (<div className='alert-box secondary'>You must save this role (above) before adding indicator permissions.</div>)
        } else { // found id -- editing
          indicatorsSection = (<div>
                                  <IndicatorDropdownMenu
                                      text='Add Indicators'
                                      icon='fa-plus'
                                      indicators={this.state.store.indicatorList}
                                      sendValue={GroupFormActions.addIndicatorSelection}>
                                  </IndicatorDropdownMenu>
                                  {indicators}
                              </div>)
        }

        var saveClasses = 'btn btn-primary'
        var saveText = 'Save Role'
        if (this.state.store.saving) {
            saveClasses += ' disabled'
            saveText = 'Saving...'
        }

        return (
            <form className='form inline user-account-container'>

                <h2>Edit Role</h2>

                <div className='row'>
                    <div className='columns small-4 left-box'>
                        <h4>Role Name</h4>
                    </div>
                    <div className='columns small-8 right-box'>
                        <input id='role_name' type='text' value={this.state.store.groupName} onChange={this.updateName} />
                    </div>
                </div>

                <div className='row'>
                    <div className='columns small-4 left-box'>
                    </div>
                    <div className='columns small-8 right-box'>
                        <button type='submit' className={saveClasses} onClick={this.submitForm}>{saveText}</button>
                    </div>
                </div>

                <hr />

                <div className='row'>
                    <div className='columns small-4 left-box'>
                        <h4>Indicator Permissions</h4>
                        <p>Changes will be saved as you make them.</p>
                    </div>
                    <div className='columns small-8 right-box'>
                        {indicatorsSection}
                    </div>
                </div>

            </form>
        )
    }
})
