var React  = require('react');
var MenuItem = require('./menuItem.jsx');
var _      = require('lodash');

function findMatches(item, re) {
	var matches = [];

	if (re.test(item.title)) {
		matches.push(item);
	}

	if (item.children) {
		item.children.forEach(function (child) {
			matches = matches.concat(findMatches(child, re));
		});
	}

	return matches;
}

module.exports = React.createClass({
	propTypes: {
		items: React.PropTypes.array.isRequired,
		searchable: React.PropTypes.bool
	},
	getInitialState: function(){
	   return {
	     open:true,
	     orientation : 'center',
	     filtered : false,
	     pattern  : ''
	   };
	},
	_toggleMenu: function(e){
	   e.preventDefault();  
	   this.setState({open:!this.state.open});
	},
	_setPattern: function(e,v1,v2){
	  this.setState({pattern:e.target.value});
	},
	_sendValue: function(val) {
	   console.log(val)
	},
	render: function(){
	   var self = this;
	   var filtered = this.state.pattern.length > 2;
	  // var pattern = (this.refs.pattern ?React.findDOMNode(this.refs.pattern).value : ''); 
	 //  console.log(pattern);
		var filteredItems;
		if (filtered) {
			filteredItems = [];
			_.forEach(this.props.items, function (item) {
				filteredItems = filteredItems.concat(findMatches(item, new RegExp(self.state.pattern, 'gi')));
			});
		} else {
			filteredItems = this.props.items;
		}
	 
	   
       var menuItems = filteredItems.map(function(item){
         return (<MenuItem 
         			key={item.id} 
         			title={item.title}
         			ancestry={item.ancestryString}
         			children={item.children}
         			value={item.value}
         			filtered={filtered}
         			depth={0}
         			sendValue={self._sendValue}
         			></MenuItem>);
       });
       
       var search = (<div role="search">
        				<input onChange={this._setPattern} type="text" />
				        <a
				       		class="clear-btn"
				       		v-on="click : clearSearch($event)"
				       		v-show="pattern.length > 0">
				       		<i class="fa fa-times-circle"></i>
				        </a>
				      </div>);
       
       var background = (<div className="background">
        					<div className="arrow"></div>
       						{this.props.searchable ? search : null}
				       	 	<ul>
				       	 		{menuItems}
				       	    </ul>
				       	 </div>);
       
	   return (<div className="menu">
	           <a
	           	className="button"
	           	onClick={this._toggleMenu} >
	   			{this.props.children}
	   			</a>
	   			<div className={this.state.orientation + " container"}>
                   {this.state.open && background}
	   			</div>
	   		   </div>);
	}
});