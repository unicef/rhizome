var React  = require('react');
var MenuItem = require('./menuItem.jsx');

module.exports = React.createClass({
	propTypes: {
		items: React.PropTypes.array.isRequired,
		searchable: React.PropTypes.bool
	},
	getInitialState: function(){
	   return {
	     open:true,
	     orientation : 'center'
	   };
	},
	render: function(){
       var menuItems = this.props.items.map(function(item){
         return (<MenuItem 
         			key={item.id} 
         			title={item.title}
         			ancestry={item.ancestryString}
         			children={item.children}
         			value={item.value}
         			></MenuItem>);
       });
       
       var search = (<div role="search">
        				<input type="text" />
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
	   			{this.props.children}
	   			<div className={this.state.orientation + " container"}>
                   {this.state.open && background}
	   			</div>
	   		   </div>);
	}
});