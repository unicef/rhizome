import React from 'react'

import api from 'utilities/api'

import d3TagsTree from './utils/d3TagsTree'

var TagsTreeAdmin = React.createClass({
  componentDidMount () {
    var el = this.getDOMNode()

    api.tagTree({}, null, {'cache-control': 'no-cache'})
      .then(response => {
        let state = { data: response.flat[0] }

        // request an animation frame. this makes sure the DOM node is rendered
        window.requestAnimationFrame(() => {
          d3TagsTree.create(el, { width: '100%', height: '500px' }, state)
        })
      })
  },

  componentWillUnmount () {
    var el = this.getDOMNode()
    d3TagsTree.destroy(el)
  },

  render () {
    return (<div className='d3-tags-tree'></div>)
  }
})

export default TagsTreeAdmin
