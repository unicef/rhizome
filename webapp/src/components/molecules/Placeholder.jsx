import React from 'react'

const Placeholder = React.createClass({
	render () {
		const height = this.props.height
		let icon_size = '5x'
		let top_offset = 68
		let	padding = '50px 0'
		if (height < 400 ) {
			icon_size = '4x'
			top_offset = 54
			padding = '40px 0'
		}
		if (height < 300 ) {
			icon_size = '3x'
			top_offset = 42
			padding = '30px 0'
		}
		if (height < 200 ) {
			icon_size = '2x'
			top_offset = 28
			padding = '20px 0'
		}
		if (height < 100 ) {
			icon_size = '1x'
			top_offset = 14
			padding = '10px 0'
		}
		return (
		  <div className='loading' style={{height: height+'px', padding: padding }}>
		    <div style={{ position: 'relative', top: (height/2)- top_offset +'px' }}>
		      <i className={'fa fa-spinner fa-spin fa-'+icon_size}></i>
		      <br />
		      Loading
		    </div>
		  </div>
		)
	}
})


export default Placeholder