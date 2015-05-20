var React  = require('react');

var MenuItem = React.createClass({
	propTypes: {
		title: React.PropTypes.string.isRequired,
		value: React.PropTypes.number.isRequired,
		ancestry: React.PropTypes.string,
		children: React.PropTypes.array
	},
	getInitialState: function () {
	    return { open: false };
	  },
	render: function(){
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
	       			></MenuItem>);
	   		});
	   } else {
	   	 children = '';
	   }
	   return (
	   	<li>
	   		{this.props.title}
	   		<div>
	   			{children}
	   		</div>	
	   	</li>
	   );
	}
});

module.exports = MenuItem;