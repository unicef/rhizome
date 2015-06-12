var React  = require('react');
var _      = require('lodash');

var MenuItem = React.createClass({
	propTypes: {
    sendValue      : React.PropTypes.func.isRequired,
    title          : React.PropTypes.string.isRequired,
    value          : React.PropTypes.number.isRequired,

    ancestryString : React.PropTypes.string,
    children       : React.PropTypes.array,
    depth          : React.PropTypes.number,
    filtered       : React.PropTypes.bool
	},

  statics : {
    fromArray : function (arr, sendValue, depth) {
      if (!_.isFinite(depth)) {
        depth = 0;
      }

      return _.map(arr, function (item) {
        return (
          <MenuItem
            key={item.value}
            depth={depth}
            sendValue={sendValue}
            {...item}>
          </MenuItem>
        );
      });
    }
  },

  getDefaultProps : function () {
    return {
      depth    : 0,
      filtered : false
    };
  },

  getInitialState: function () {
      return { open: false };
  },

  _toggleChildren: function(e) {
    e.stopPropagation();
    this.setState({open:!this.state.open});
  },

  _handleClick: function(e){
    this.props.sendValue(this.props.value);
  },

	render: function(){
	   var self = this;
	   //COMPUTED PROPERTIES
	   var hasChildren = !this.props.filtered && _.isArray(this.props.children) && this.props.children.length > 0;
	   var itemStyle = {'paddingLeft':(this.state.filtered?'5px': (5 + (17 * this.props.depth)) + 'px')};

	   var children = null;
     if(this.props.children && this.state.open) {
	     children = MenuItem.fromArray(
        this.props.children,
        this.props.sendValue,
        this.props.depth + 1);
	   }

     var prefix = this.props.filtered ? _.get(this.props, 'ancestryString', '') : '';
     var title  = prefix + this.props.title;

	   return (
	   	<li>
   	    	<a
   	    		role="menuitem"
   	    		onClick={this._handleClick}
   	    		style={itemStyle}
   	    		className={(hasChildren?"folder":null)}
            tabIndex='-1'>

   	    		<i
   	    			className={"fa fa-lg fa-fw " + (this.state.open?"fa-caret-down":"fa-caret-right")}
   	    			onClick={this._toggleChildren}></i>

   	    		{title}
   	    	</a>

	   		<div>
	   			{children}
	   		</div>
	   	</li>
	   );
	}
});

module.exports = MenuItem;
