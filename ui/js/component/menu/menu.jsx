var React  = require('react');
var MenuItem = require('./menuItem.jsx');
var _      = require('lodash');
var dom = require('util/dom');

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
		searchable: React.PropTypes.bool,
		sendValue: React.PropTypes.func
	},
	getInitialState: function(){
	   return {
	     open:false,
	     orientation : 'center',
	     maxHeight   : 'none',
	     marginLeft  : 0,
	     filtered : false,
	     pattern  : ''
	   };
	},
	componentDidMount: function(){
	  window.addEventListener('resize', this._onResize);
	  window.addEventListener('scroll', this._onResize);
	  this._onResize();
	},
	_toggleMenu: function(e){
	   e.stopPropagation(); 
	   this.setState({open:!this.state.open},this._onResize);
	   window.addEventListener('click', this._onClick);
	},
	_onClick: function(e){
	  this.setState({open:false});
	  this.setState({pattern:''});
	},
	_setPattern: function(e){
	  this.setState({pattern:e.target.value});
	},
	_clearSearch: function(e){
	   e.stopPropagation(); 
	   this.setState({pattern:''});
	},
	_onResize : function () {

		var el     = dom.dimensions(React.findDOMNode(this.refs.el));
        var menu   = dom.dimensions(React.findDOMNode(this.refs.menu));
		var items  = (this.refs.itemlist ? dom.dimensions(React.findDOMNode(this.refs.itemlist)) : {height:0});
		var offset = dom.viewportOffset(React.findDOMNode(this.refs.el));

		this.setState({'maxHeight': window.innerHeight - offset.top - (menu.height - items.height)});

		var rightEdge = offset.left + (el.width / 2) + (menu.width / 2);
		var leftEdge  = offset.left + (el.width / 2) - (menu.width / 2);

		if (menu.width > window.innerWidth) {
			this.setState({'orientation':'left'});
			this.setState({'marginLeft':0});
		} else if (el.width >= menu.width) {
			this.setState({'orientation':'center'});
			this.setState({'marginLeft':-menu.width / 2});
		} else if (leftEdge < 0) {
			this.setState({'orientation':'left'});
			this.setState({'marginLeft':0});
		} else if (rightEdge > window.innerWidth) {
			this.setState({'orientation':'right'});
			this.setState({'marginLeft':0});
		} else {
			this.setState({'orientation':'center'});
			this.setState({'marginLeft':-menu.width / 2});
		}
	},
	render: function(){
	   var self = this;
	   var filtered = this.state.pattern.length > 2;
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
         			key={item.value} 
         			title={item.title}
         			ancestry={item.ancestryString}
         			children={item.children}
         			value={item.value}
         			filtered={filtered}
         			depth={0}
         			sendValue={self.props.sendValue}
         			></MenuItem>);
       });
       
       var clearSearch = (<a
				       		className="clear-btn"
				       		onClick={this._clearSearch}>
				       		<i className="fa fa-times-circle"></i>
				       		</a>);
       
       var search = (<div role="search">
        				<input onChange={this._setPattern} onClick={function(e){e.stopPropagation();}} value={this.state.pattern} type="text" />
				      {this.state.pattern.length>0 ? clearSearch:null}
				      </div>);
       
       var itemlistStyle = {"maxHeight" : this.state.maxHeight};
       var background = (<div className="background">
        					<div className="arrow"></div>
       						{this.props.searchable ? search : null}
				       	 	<ul ref="itemlist" style={itemlistStyle}>
				       	 		{menuItems}
				       	    </ul>
				       	 </div>);
       
       var containerStyle = {marginLeft : this.state.marginLeft + 'px'};
       
	   return (<div className="menu" ref="el">
	           <a
	           	className="button"
	           	onClick={this._toggleMenu} >
	   			{this.props.children}
	   			</a>
	   			<div className={this.state.orientation + " container"}
	   			     style={containerStyle}
	   			     ref="menu"
	   			     >
                     {this.state.open ? background:null}
	   			</div>
	   		   </div>);
	}
});