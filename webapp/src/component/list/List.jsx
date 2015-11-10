var React = require('react')

module.exports = React.createClass({
    propTypes: {
        items: React.PropTypes.arrayOf(React.PropTypes.object).isRequired, // [{id:1,title:'abc'},...]
        removeItem: React.PropTypes.func.isRequired
    },
    render: function (){
        var self = this
        var listItems = this.props.items.map(function (item){
             return (<li key={item.id}>{item.name}
                        <a
                        className='clear-btn'
                        onClick={self.props.removeItem.bind(this,item.id)}>
                            <i className='fa fa-times-circle'></i>
                        </a>
                    </li>)
        })
        return <ul className='list'>{listItems}</ul>
    }
})
