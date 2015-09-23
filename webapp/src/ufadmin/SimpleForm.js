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
    var tag_form_data, bound_form_data, calc_form_data = {};

    // console.log('this dot props: ', this.props)
    // console.log('this dot state : ', this.state)

    var indicatorId  = this.props.params.id
    var indicatorObject  = this.state.store.indicatorObject
    var allTags = this.state.store.indTags;

    // CASE 1 ->  There is an id in the url but the request is still pending //
    if (indicatorId && !indicatorObject){
      return <div>'LOADING'</div>
    }

    // CASE 2 -> no object_id: load only the base form for this model
    // render a create form with none of the additional components //
    if (!indicatorId){
        var form_welcome_text = 'Create a New Indicator Below'
        base_form_data = {
            name: "",
            short_name: ''
        };
    }

    // CASE 3 -> He have the object - render the 3 component forms for indicator
    else {
        var form_welcome_text = 'Update Indicator: ' + indicatorObject.short_name
        var base_form_data = {name: indicatorObject.name, short_name: indicatorObject.short_name}
        var tag_form_data = indicatorObject.tag_json;
        var bound_form_data = {};
        var calc_form_data = {};
    };

    var base_form_settings = {
        form: true,
    };

    var tag_form_settings = {
        form: true,
        fields: { tag_json: {type: 'array'} }
    };

    var base_form = <div>
        <p className="pageWelcome"> {form_welcome_text} </p>
        <ReactJson value={ base_form_data } settings={ base_form_settings }/>,
      </div>;

    var tag_rows =[]
    _.forEach(tag_form_data, function(tag_id) {
        var tag_name = _.find(allTags, function(t) { return t.id === tag_id }).tag_name;
        var delete_btn = <span className="fa fa-times"></span>
        var tag_row = <li> {tag_name} ({tag_id}) {delete_btn} </li>
        tag_rows.push(tag_row)
        return tag_row;
    });

    var tag_form = <div>
        <p className="pageWelcome"> some tag data </p>
          <ul>
            {tag_rows}
          </ul>
      </div>;

    return (
      <div className="row">
        <div className="small-8 columns">
          {base_form}
        </div>
        <div className="small-4 columns">
          {tag_form}
        </div>
      </div>
    );
  }
});

module.exports = SimpleForm;


// module.exports = {
// 	template: require('./template.html'),
// 	data: function(){
// 	  return {
// 		locations:[],
// 		groups:[]
// 	  };
// 	},
// 	created: function() {
// 	  var self = this;
//
// 	  self.$set('tagLoading',true);
//
// 		// load indicators in the table
// 		self.loadIndicatorTag();
//
// 		// render tag tree dropdown
// 		api.tagTree() //
// 			.then(function(response) {
// 				var ddProps = {
// 					tag_tree: response.objects,
// 					text: 'Add Tag',
// 					sendValue: self.addTagToIndicator
// 				};
// 				self.indicatorDropdown = React.render(React.createElement(IndicatorTagDropdownMenu, ddProps), document.getElementById("tagSelector"));
// 			});
//
// 	},
// 		addTagToIndicator: function(data){
// 	    var self = this;
// 	    self.$set('tagLoading',true);
// 	    api.set_indicator_to_tag( {indicator_id:this.$parent.$data.indicator_id, indicator_tag_id:data }).then(function(){
// 	      self.loadIndicatorTag();
// 	    });
// 	  },
// 	  deleteTagFromIndicator: function(data){
// 	    var self = this;
// 	    api.set_indicator_to_tag( {indicator_id:this.$parent.$data.indicator_id, indicator_tag_id:data
// 				,id:'' }).then(function(){
// 	      self.loadIndicatorTag();
// 	    });
// 	  },
// 	  loadIndicatorTag: function(){
// 			// first load the tags, then map the values of the given indicator //
// 	    var self = this;
// 	    self.$set('tagLoading',true);
//
// 			api.indicator_tag().then(function(data){
// 				var tag_map = [];
// 				var indicator_tags = data.objects;
// 				_.forEach(indicator_tags,function(tag){
// 					tag_map[tag.id] = tag.tag_name;
// 				});
// 				self.$set('tag_map',tag_map);
// 			});
//
// 			api.indicator_to_tag({indicator_id:this.$parent.$data.indicator_id},null,{'cache-control':'no-cache'}).then(function(data){
// 				var indicator_tags = data.objects;
// 				_.forEach(indicator_tags,function(indicator_tag){
// 				   indicator_tag.tag_name = self.tag_map[indicator_tag.indicator_tag_id];
// 				 });
// 				self.$set('indicator_tags',indicator_tags);
// 				self.$set('tagLoading',false);
// 			});
// 		},
// 	}
// };
