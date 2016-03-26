import React, {PropTypes} from 'react'

const Placeholder = React.createClass({

  propTypes: {
    height: PropTypes.number,
    text: PropTypes.string,
    loading: PropTypes.bool
  },

  getDefaultProps() {
    return {
    	text: 'No Data',
    	height: null,
    	loading: true
    }
  },

	render () {
		const height = this.props.height
		const loading = this.props.loading

		let icon_size = '5x'
		let top_offset = 68
		let	padding = '50px 0'
		let	font_size = '1.8rem'
		if (height < 400 ) {
			icon_size = '4x'
			top_offset = 54
			padding = '40px 0'
			font_size = '1.6rem'
		}
		if (height < 300 ) {
			icon_size = '3x'
			top_offset = 42
			padding = '30px 0'
			font_size = '1.4rem'
		}
		if (height < 200 ) {
			icon_size = '2x'
			top_offset = 28
			padding = '20px 0'
			font_size = '1.2rem'
		}
		if (height < 100 ) {
			icon_size = '1x'
			top_offset = 14
			padding = '10px 0'
			font_size = '1rem'
		}

		const container_styles = height ? { height: height+'px', padding: padding } : {}
		const spinner_styles = height ? { position: 'relative', top: (height/2)- top_offset +'px' } : {}

		return (
		  <div className='loading' style={container_styles}>
		    <div style={spinner_styles}>
		    	{ loading ? <i className={'fa fa-spinner fa-spin fa-'+icon_size}></i> : '' }
		      <br />
		      <span style={{fontSize: font_size}}>
			    	{ loading ? 'Loading...' : this.props.text }
		      </span>
		    </div>
		  </div>
		)
	}
})


export default Placeholder