'use strict';
var _      = require('lodash');
var moment = require('moment');
var React  = require('react');
var Reflux = require('reflux');
var ReactJson = require('react-json')
var SimpleFormStore = require('stores/SimpleFormStore');
var SimpleFormActions = require('actions/SimpleFormActions');
var ReactRouter = require('react-router')
var { Route, Router} = ReactRouter;


var SimpleForm = React.createClass({
  mixins: [
    Reflux.connect(SimpleFormStore, 'store'),
    // ReactRouter.State ,
  ],

  contextTypes: {
    router: React.PropTypes.func
  },

  getInitialState : function () {
    return {
    };
  },

  componentWillMount: function() {
    console.log('query indicators for id: ',this.props.params.id)
    SimpleFormActions.initialize(this.props.params.id)
	},

  render : function () {

    // console.log('this dot props: ', this.props)
    // console.log('this dot state : ', this.state)

    var indicatorId  = this.props.params.id
    var indicatorObject  = this.state.store.indicatorObject
    console.log('indicatorObject : ', indicatorObject)

    if (indicatorId && !indicatorObject){
      return <div>'LOADING'</div>
    }

    var doc = indicatorObject
    if (!indicatorId){ // render a create form //
      var doc = {
          name: "HI THIS IS JOIN ",
          short_name: 'john'
      };
    }

    https://github.com/arqex/react-json/blob/master/docs/baseFieldTypes.md#array
    var settings = {
        form: true,
        fields: { short_name: {type: 'text'} }
    };

    return (
      <div className="row">
        <div className="small-8 columns">
          <p className="pageWelcome">
            Create an Indicator Below
          </p>
          <form>
            <ReactJson value={ doc } settings={ settings }/>,
          </form>
        </div>
      </div>
    );
  }
});

module.exports = SimpleForm;
