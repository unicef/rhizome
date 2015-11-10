'use strict'

var React = require('react')

var HomepageCarouselDecorators = [
  {
    component: React.createClass({
      render () {
        return (
            <div className='navigator-button'
                 style={this.getButtonStyles(this.props.currentSlide === 0)}
                 onClick={this.props.previousSlide}>
              <i className='fa fa-chevron-left'></i>
            </div>
        )
      },
      getButtonStyles (disabled) {
        return {
          opacity: disabled ? 0.3 : 0.7
        }
      }
    }),
    position: 'CenterLeft'
  },
  {
    component: React.createClass({
      render () {
        return (
            <div className='navigator-button'
                 style={this.getButtonStyles(this.props.currentSlide + this.props.slidesToScroll >= this.props.slideCount)}
                 onClick={this.props.nextSlide}>
              <i className='fa fa-chevron-right'></i>
            </div>
        )
      },
      getButtonStyles (disabled) {
        return {
          opacity: disabled ? 0.3 : 0.7
        }
      }
    }),
    position: 'CenterRight'
  },
  {
    component: React.createClass({
      render () {
        var self = this
        var indexes = this.getIndexes(self.props.slideCount, self.props.slidesToScroll)
        return (
          <ul style={self.getListStyles()}>
            {
              indexes.map(function (index) {
                return (
                  <li style={self.getListItemStyles()} key={index}>
                    <button
                      style={self.getButtonStyles(self.props.currentSlide === index)}
                      onClick={self.props.goToSlide.bind(null, index)}>
                      &bull
                    </button>
                  </li>
                )
              })
            }
          </ul>
        )
      },
      getIndexes (count, inc) {
        var arr = []
        for (var i = 0; i < count; i += inc) {
          arr.push(i)
        }
        return arr
      },
      getListStyles () {
        return {
          position: 'relative',
          margin: 0,
          top: 25,
          padding: 0
        }
      },
      getListItemStyles () {
        return {
          listStyleType: 'none',
          display: 'inline-block'
        }
      },
      getButtonStyles (active) {
        return {
          border: 0,
          background: 'transparent',
          color: '#BCBCBC',
          cursor: 'pointer',
          padding: 0,
          outline: 0,
          fontSize: 36,
          opacity: active ? 1 : 0.5
        }
      }
    }),
    position: 'BottomCenter'
  }
]

module.exports = HomepageCarouselDecorators

