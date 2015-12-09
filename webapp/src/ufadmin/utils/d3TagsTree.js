import api from '../../data/api'
import d3 from 'd3'

var duration = 750
var panSpeed = 200
var panBoundary = 20 // Within 20px from edges will pan when dragging

var tt = {}

function toggleChildren (d) {
  if (d.children) {
    d._children = d.children
    d.children = null
  } else if (d._children) {
    d.children = d._children
    d._children = null
  }
  return d
}

function expand (d) {
  if (d._children) {
    d.children = d._children
    d.children.forEach(expand)
    d._children = null
  }
}

// A recursive helper function for performing some setup by walking through all nodes
function visit (parent, visitFn, childrenFn) {
  if (!parent) return

  visitFn(parent)

  var children = childrenFn(parent)
  if (children) {
    var count = children.length
    for (var i = 0; i < count; i++) {
      visit(children[i], visitFn, childrenFn)
    }
  }
}

tt.create = function (el, props, state) {
  var svg = d3.select(el).append('svg')
              .attr('class', 'd3')
              .attr('width', props.width)
              .attr('height', props.height)

  tt.svgGroup = svg.append('g').attr('class', 'd3-svg-g')

  tt.viewerWidth = el.offsetWidth
  tt.viewerHeight = el.offsetHeight
  tt.tree = d3.layout.tree().size([tt.viewerHeight, tt.viewerWidth])
  tt.diagonal = d3.svg.diagonal().projection(function (d) { return [d.y, d.x] })
  tt.zoomListener = d3.behavior.zoom().scaleExtent([0.1, 3]).on('zoom', tt._zoom)

  svg.call(tt.zoomListener)

  tt.root = state.data
  tt.root.x0 = tt.viewerHeight / 2
  tt.root.y0 = 0

  tt.draggingNode = null
  tt.selectedNode = null
  tt.dragStarted = false
  tt.domNode = null

  tt._sortTree()

  // Call visit function to establish maxLabelLength
  tt.maxLabelLength = 0
  visit(state.data,
    function (d) {
      tt.maxLabelLength = Math.max(d.title.length, tt.maxLabelLength)
    },
    function (d) {
      return d.children && d.children.length > 0 ? d.children : null
    }
  )

  tt._update(tt.root)
  tt._initialPan()
//  tt._centerNode(tt.root)
}

tt.update = function (el, props, state) {
  tt._update(tt.root)
}

tt.destroy = function (el) {
}

tt._update = function (source) {
  // Compute the new height, function counts total children of root node and sets tree height accordingly.
  // This prevents the layout looking squashed when new nodes are made visible or looking sparse when nodes are removed
  // This makes the layout more consistent.
  var levelWidth = [1]
  var childCount = function (level, n) {
    if (n.children && n.children.length > 0) {
      if (levelWidth.length <= level + 1) levelWidth.push(0)
      levelWidth[level + 1] += n.children.length
      n.children.forEach(function (d) {
        childCount(level + 1, d)
      })
    }
  }
  childCount(0, tt.root)
  var newHeight = d3.max(levelWidth) * 25 // 25 pixels per line
  tt.tree = tt.tree.size([newHeight, tt.viewerWidth])

  // Compute the new tree layout.
  var nodes = tt.tree.nodes(tt.root).reverse()
  let links = tt.tree.links(nodes)

  // Set widths between levels based on maxLabelLength.
  nodes.forEach(function (d) {
    d.y = (d.depth * (tt.maxLabelLength * 10)) // maxLabelLength * 10px

    // alternatively to keep a fixed scale one can set a fixed depth per level
    // Normalize for fixed-depth by commenting out below line
    // d.y = (d.depth * 500) //500px per level.
  })

  // Update the nodes…
  var i = 0
  var node = tt.svgGroup.selectAll('g.node').data(nodes, function (d) {
    return d.id || (d.id = ++i)
  })

  var dragListener = d3.behavior.drag()
    .on('dragstart', function (d) {
      if (d === tt.root) return
      tt.dragStarted = true
      nodes = tt.tree.nodes(d)
      d3.event.sourceEvent.stopPropagation()
      // it's important that we suppress the mouseover event on the node being dragged. Otherwise it will absorb the mouseover event and the underlying node will not detect it d3.select(this).attr('pointer-events', 'none')
    })
    .on('drag', function (d) {
      if (d === tt.root) return
      if (tt.dragStarted) {
        tt.domNode = this
        tt._initiateDrag(d, tt.domNode)
      }

      // get coords of mouseEvent relative to svg container to allow for panning
      var s = d3.select('svg')
      var relCoords = d3.mouse(s[0][0])
      var w = +s.style('width').replace('px', '')
      var h = +s.style('height').replace('px', '')

      if (relCoords[0] < panBoundary) {
        tt.panTimer = true
        tt._pan(this, 'left')
      } else if (relCoords[0] > (w - panBoundary)) {
        tt.panTimer = true
        tt._pan(this, 'right')
      } else if (relCoords[1] < panBoundary) {
        tt.panTimer = true
        tt._pan(this, 'up')
      } else if (relCoords[1] > (h - panBoundary)) {
        tt.panTimer = true
        tt._pan(this, 'down')
      } else {
        try {
          clearTimeout(tt.panTimer)
        } catch (e) {}
      }

      d.x0 += d3.event.dy
      d.y0 += d3.event.dx
      var node = d3.select(this)
      node.attr('transform', 'translate(' + d.y0 + ',' + d.x0 + ')')
      tt._updateTempConnector()
    })
    .on('dragend', function (d) {
      if (d === tt.root) return
      tt.domNode = this
      if (tt.selectedNode) {
        // now remove the element from the parent, and insert it into the new elements children
        var index = tt.draggingNode.parent.children.indexOf(tt.draggingNode)
        if (index > -1) {
          tt.draggingNode.parent.children.splice(index, 1)
        }

        if (typeof tt.selectedNode.children !== 'undefined' || typeof tt.selectedNode._children !== 'undefined') {
          if (typeof tt.selectedNode.children !== 'undefined') {
            tt.selectedNode.children.push(tt.draggingNode)
          } else {
            tt.selectedNode._children.push(tt.draggingNode)
          }
        } else {
          tt.selectedNode.children = []
          tt.selectedNode.children.push(tt.draggingNode)
        }
        // Make sure that the node being added to is expanded so user can see added node is correctly moved
        expand(tt.selectedNode)
        tt._sortTree()
        tt._endDrag()
      } else {
        tt._endDrag()
      }
    })

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append('g')
    .call(dragListener)
    .attr('class', 'node')
    .attr('transform', function (d) {
      return 'translate(' + source.y0 + ',' + source.x0 + ')'
    })
    .on('click', tt._click)

  nodeEnter.append('circle')
    .attr('class', 'nodeCircle')
    .attr('r', 0)
    .style('fill', function (d) {
      return d._children ? 'lightsteelblue' : '#fff'
    })

  nodeEnter.append('text')
    .attr('x', function (d) {
      return d.children || d._children ? -10 : 10
    })
    .attr('dy', '.35em')
    .attr('class', 'nodeText')
    .attr('text-anchor', function (d) {
      return d.children || d._children ? 'end' : 'start'
    })
    .text(function (d) {
      return d.title
    })
    .style('fill-opacity', 0)

  // phantom node to give us mouseover in a radius around it
  nodeEnter.append('circle')
    .attr('class', 'ghostCircle')
    .attr('r', 30)
    .attr('opacity', 0.2) // change this to zero to hide the target area
    .style('fill', 'red')
    .attr('pointer-events', 'mouseover')
    .on('mouseover', function (node) {
      tt._inCircle(node)
    })
    .on('mouseout', function (node) {
      tt._outCircle(node)
    })

  // Update the text to reflect whether node has children or not.
  node.select('text')
    .attr('x', function (d) {
      return d.children || d._children ? -10 : 10
    })
    .attr('text-anchor', function (d) {
      return d.children || d._children ? 'end' : 'start'
    })
    .text(function (d) {
      return d.title
    })

  // Change the circle fill depending on whether it has children and is collapsed
  node.select('circle.nodeCircle')
    .attr('r', 4.5)
    .style('fill', function (d) {
      return d._children ? 'lightsteelblue' : '#fff'
    })

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
    .duration(duration)
    .attr('transform', function (d) {
      return 'translate(' + d.y + ',' + d.x + ')'
    })

  // Fade the text in
  nodeUpdate.select('text')
    .style('fill-opacity', 1)

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
    .duration(duration)
    .attr('transform', function (d) {
      return 'translate(' + source.y + ',' + source.x + ')'
    })
    .remove()

  nodeExit.select('circle')
    .attr('r', 0)

  nodeExit.select('text')
    .style('fill-opacity', 0)

  // Update the links…
  var link = tt.svgGroup.selectAll('path.link')
    .data(links, function (d) {
      return d.target.id
    })

  // Enter any new links at the parent's previous position.
  link.enter().insert('path', 'g')
    .attr('class', 'link')
    .attr('d', function (d) {
      var o = {
        x: source.x0,
        y: source.y0
      }
      return tt.diagonal({
        source: o,
        target: o
      })
    })

  // Transition links to their new position.
  link.transition()
    .duration(duration)
    .attr('d', tt.diagonal)

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
    .duration(duration)
    .attr('d', function (d) {
      var o = {
        x: source.x,
        y: source.y
      }
      return tt.diagonal({
        source: o,
        target: o
      })
    })
    .remove()

  // Stash the old positions for transition.
  nodes.forEach(function (d) {
    d.x0 = d.x
    d.y0 = d.y
  })
}

tt._click = function (d) {
  if (d3.event.defaultPrevented) return // click suppressed
  d = toggleChildren(d)
  tt._update(d)
  tt._centerNode(d)
}

tt._inCircle = function (d) {
  tt.selectedNode = d
  tt._updateTempConnector()
}

tt._outCircle = function (d) {
  tt.selectedNode = null
  tt._updateTempConnector()
}

// Function to update the temporary connector indicating dragging affiliation
tt._updateTempConnector = function () {
  var data = []
  if (tt.draggingNode !== null && tt.selectedNode !== null) {
    // have to flip the source coordinates since we did this for the existing connectors on the original tree
    data = [{
      source: {
        x: tt.selectedNode.y0,
        y: tt.selectedNode.x0
      },
      target: {
        x: tt.draggingNode.y0,
        y: tt.draggingNode.x0
      }
    }]
  }
  var link = tt.svgGroup.selectAll('.templink').data(data)
  link.enter().append('path')
    .attr('class', 'templink')
    .attr('d', d3.svg.diagonal())
    .attr('pointer-events', 'none')

  link.attr('d', d3.svg.diagonal())

  link.exit().remove()
}

tt._initiateDrag = function (d, domNode) {
  tt.draggingNode = d
  d3.select(tt.domNode).select('.ghostCircle').attr('pointer-events', 'none')
  d3.selectAll('.ghostCircle').attr('class', 'ghostCircle show')
  d3.select(tt.domNode).attr('class', 'node activeDrag')

  tt.svgGroup.selectAll('g.node').sort(function (a, b) { // select the parent and sort the path's
    if (a.id !== tt.draggingNode.id) return 1 // a is not the hovered element, send 'a' to the back
    else return -1 // a is the hovered element, bring 'a' to the front
  })
  // if nodes has children, remove the links and nodes
  var nodes = tt.tree.nodes(d)
  if (nodes.length > 1) {
    // remove link paths
    var links = tt.tree.links(nodes)
      .data(links, function (d) {
        return d.target.id
      }).remove()
    // remove child nodes
    tt.svgGroup.selectAll('g.node')
      .data(nodes, function (d) {
        return d.id
      }).filter(function (d, i) {
        if (d.id === tt.draggingNode.id) {
          return false
        }
        return true
      }).remove()
  }

  tt.svgGroup.selectAll('path.link').filter(function (d, i) {
    if (d.target.id === tt.draggingNode.id) {
      return true
    }
    return false
  }).remove()

  tt.dragStarted = null
}

tt._endDrag = function () {
  if (tt.selectedNode !== null && tt.draggingNode !== null) {
    var fetch = api.post_indicator_tag
    fetch({ id: tt.draggingNode.id, tag_name: tt.draggingNode.tag_name, parent_tag_id: tt.selectedNode.id })
  }

  tt.selectedNode = null
  d3.selectAll('.ghostCircle').attr('class', 'ghostCircle')
  d3.select(tt.domNode).attr('class', 'node')
  // now restore the mouseover event or we won't be able to drag a 2nd time
  d3.select(tt.domNode).select('.ghostCircle').attr('pointer-events', '')
  tt._updateTempConnector()
  if (tt.draggingNode !== null) {
    tt._update(tt.root)
    tt._centerNode(tt.draggingNode)
    tt.draggingNode = null
  }
}

tt._centerNode = function (source) {
  var scale = tt.zoomListener.scale()
  var x = -source.y0
  var y = -source.x0
  x = x * scale + tt.viewerWidth / 2
  y = y * scale + tt.viewerHeight / 2
  d3.select('g').transition()
    .duration(duration)
    .attr('transform', 'translate(' + x + ',' + y + ')scale(' + scale + ')')
  tt.zoomListener.scale(scale)
  tt.zoomListener.translate([x, y])
}

tt._zoom = function () {
  tt.svgGroup.attr('transform', 'translate(' + d3.event.translate + ')scale(' + d3.event.scale + ')')
}

tt._pan = function (domNode, direction) {
  var speed = panSpeed
  if (tt.panTimer) {
    clearTimeout(tt.panTimer)
    var translateCoords = d3.transform(tt.svgGroup.attr('transform'))
    var translateX, translateY
    if (direction === 'left' || direction === 'right') {
      translateX = direction === 'left' ? translateCoords.translate[0] + speed : translateCoords.translate[0] - speed
      translateY = translateCoords.translate[1]
    } else if (direction === 'up' || direction === 'down') {
      translateX = translateCoords.translate[0]
      translateY = direction === 'up' ? translateCoords.translate[1] + speed : translateCoords.translate[1] - speed
    }
    var scale = tt.zoomListener.scale()
    tt.svgGroup.transition().attr('transform', 'translate(' + translateX + ',' + translateY + ')scale(' + scale + ')')
    d3.select(tt.domNode).select('g.node').attr('transform', 'translate(' + translateX + ',' + translateY + ')')
    tt.zoomListener.scale(tt.zoomListener.scale())
    tt.zoomListener.translate([translateX, translateY])
    tt.panTimer = setTimeout(function () {
      tt._pan(domNode, direction)
    }, 50)
  }
}

tt._sortTree = function () {
  tt.tree.sort(function (a, b) {
    return b.title.toLowerCase() < a.title.toLowerCase() ? 1 : -1
  })
}

tt._initialPan = function () {
  var source = tt.root
  var scale = tt.zoomListener.scale()
  var x = -source.y0
  var y = -source.x0
  x = x * scale + tt.viewerWidth / 10
  y = y * scale + tt.viewerHeight / 2
  d3.select('g').transition()
    .duration(duration)
    .attr('transform', 'translate(' + x + ',' + y + ')scale(' + scale + ')')
  tt.zoomListener.scale(scale)
  tt.zoomListener.translate([x, y])
}

export default tt
