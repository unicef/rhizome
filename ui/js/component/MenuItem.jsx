var React  = require('react');
var _      = require('lodash');

var MenuItem = React.createClass({
	propTypes: {
		title: React.PropTypes.string.isRequired,
		value: React.PropTypes.number.isRequired,
		ancestry: React.PropTypes.string,
		children: React.PropTypes.array,
		depth: React.PropTypes.number,
		sendValue: React.PropTypes.func
	},

  statics : {
    fromArray : function (arr, sendValue) {
      return _.map(arr, function (item) {
        return (
          <MenuItem
            key={item.value}
            title={item.title}
            ancestry={item.ancestryString}
            children={item.children}
            value={item.value}
            depth={0}
            sendValue={sendValue}>
          </MenuItem>
        );
      });
    }
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

	   var children;
       if(this.props.children && this.state.open)
	   {
	     children = this.props.children.map(function(item){
	       return (<MenuItem
	       			key={item.value}
	       			title={item.title}
	       			ancestry={item.ancestryString}
	       			children={item.children}
	       			value={item.value}
	       			filtered={self.props.filtered}
	       			depth={self.props.depth + 1}
	       			sendValue={self.props.sendValue}
	       			></MenuItem>);
	   		});
	   } else {
	   	 children = '';
	   }
	   return (
	   	<li>
   	    	<a
   	    		role="menuitem"
   	    		 onClick={this._handleClick}
   	    		style={itemStyle}
   	    		className={(hasChildren?"folder":null)} >

   	    		<i

   	    			className={"fa fa-lg fa-fw " + (this.state.open?"fa-caret-down":"fa-caret-right")}

   	    			onClick={this._toggleChildren}></i>
   	    		<span >{this.props.ancestryString}</span>
   	    		{this.props.title}
   	    	</a>

	   		<div>
	   			{children}
	   		</div>
	   	</li>
	   );
	}
});

module.exports = MenuItem;
