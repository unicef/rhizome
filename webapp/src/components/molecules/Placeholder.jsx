import React from 'react'

const Placeholder = React.createClass({
	render () {
		return (
		  <div className='loading' style={{height: this.props.height+'px' }}>
		    <div style={{ position: 'relative', top: (this.props.height/2)- 68 +'px' }}>
		      <i className='fa fa-spinner fa-spin fa-5x'></i>
		      <br />
		      Loading
		    </div>
		  </div>
		)
	}
})


export default Placeholder