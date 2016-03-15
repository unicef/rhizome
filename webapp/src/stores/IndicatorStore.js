import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import IndicatorActions from 'actions/IndicatorActions'
import treeify from 'data/transform/treeify'

var IndicatorStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: IndicatorActions,

  indicators: {
    meta: null,
    raw: null,
    index: null,
    filtered: [],
    list: [],
    selected: [],
    tree: []
  },

  init () {
    IndicatorActions.fetchIndicators()
    IndicatorActions.fetchIndicatorTags()
  },

  getInitialState () {
    return this.indicators
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ============================  Fetch Indicators  =========================== //
  onFetchIndicators () {
    this.setState({ raw: [] })
  },
  onFetchIndicatorsCompleted (response) {
    this.indicators.meta = response.meta
    this.indicators.raw = response.objects
    this.indicators.filtered = this.indicators.raw
    this.indicators.index = _.indexBy(this.indicators.raw, 'id')
    this.processIndicators()
  },
  onFetchIndicatorsFailed (error) {
    this.setState({ error: error })
  },

  // ===========================  Fetch Indicator Tags ========================= //
  onFetchIndicatorTags () {
    this.setState({ raw: [] })
  },
  onFetchIndicatorTagsCompleted (response) {
    this.indicators.tags = response.objects
    this.processIndicators()
  },
  onFetchIndicatorTagsFailed (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                            REGULAR ACTION HANDLERS                          //
  // =========================================================================== //
  onSelectIndicators (indicator_ids) {
    if (Array.isArray(indicator_ids)) {
      this.setState({ selected: indicator_ids.map(id => this.indicators.index[id]) })
    } else {
      this.setState({ selected: [this.indicators.index[indicator_ids]] })
    }
  },
  onSelectIndicator (id) {
    this.indicators.selected.push(this.indicators.index[id])
    this.trigger(this.indicators)
  },
  onDeselectIndicator (id) {
    _.remove(this.indicators.selected, {id: id})
    this.trigger(this.indicators)
  },
  onReorderIndicator (selected_indicators) {
    this.indidcators.selected = selected_indicators
    this.trigger(this.indicators)
  },
  onClearSelectedIndicators (id) {
    this.indicators.selected = []
    this.trigger(this.indicators)
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  processIndicators () {
    if (this.indicators.raw && this.indicators.tags) {
      this.indicators.tree = this.buildIndicatorsTree(this.indicators.raw, this.indicators.tags, true, true)
      this.indicators.list = _.sortBy(this.indicators.tree, 'title')
      this.setState(this.indicators)
    }
  },

  makeTagId (tId) {
    return 'tag-' + tId
  },

  pickAllNodesInTrees (parent, nodes) {
    let children = parent.children
    if (children && children.length) {
      children.forEach(item => this.pickAllNodesInTrees(item, nodes))
    } else {
      if (parent.noValue) nodes.push(parent)
    }
  },

  removeIndicatorEmptyNode (sourceList) {
    if (!sourceList || !sourceList.length) {
      return sourceList
    }

    let virtualRoot = {noValue: false, parentNode: null, title: 'No Available Indicator', children: sourceList}
    virtualRoot.children.forEach(item => item.parentNode = virtualRoot)

    let nodes
    do {
      nodes = []
      this.pickAllNodesInTrees(virtualRoot, nodes)
      nodes.forEach(item => item.parentNode.children.splice(item.parentNode.children.indexOf(item), 1))
    } while (nodes.length > 0)

    if (sourceList.length > 0) {
      return sourceList
    } else {
      virtualRoot.noValue = true
      virtualRoot.children = []
      return [virtualRoot]
    }
  },

  buildIndicatorsTree (indicators, tags, isClone, isRemoveEmpty, indicatorFilterType) {
    if (isClone) {
      tags = _.cloneDeep(tags)
      indicators = _.cloneDeep(indicators)
    }

    let sortTags = _.sortBy(tags, 'tag_name').reverse()

    let tags_map = {}
    sortTags.forEach(tag => {
      tags_map[tag.id] = tag
      tag.id = this.makeTagId(tag.id)
      tag.noValue = true
      tag.parent = tag.parent_tag_id && tag.parent_tag_id !== 'None' ? this.makeTagId(tag.parent_tag_id) : null
      tag.children = []
      tag.title = tag.tag_name
      tag.value = tag.id
    })

    // add 'Other Indicators' tag to collect any indicators without tags
    const otherTag = {
      'id': 0,
      'value': this.makeTagId(0),
      'noValue': true,
      'title': 'Other Indicators',
      'children': []
    }

    indicators.forEach(indicator => {
      indicator.title = indicator.name
      indicator.value = indicator.id
      indicator.displayTitle = indicator.name + ' (' + indicator.id + ')'
      if (indicatorFilterType) {
        if (!_.isArray(indicator.tag_json) || indicator.tag_json.length === 0) {
          if (indicatorFilterType && indicator.data_format === indicatorFilterType) {
            otherTag.children.push(indicator)
            indicator.parentNode = otherTag
          }
        } else if (_.isArray(indicator.tag_json)) {
          indicator.tag_json.forEach(tId => {
            if (indicatorFilterType && indicator.data_format === indicatorFilterType) {
              let tagParent = tags_map[tId]
              tagParent.children.push(indicator)
              indicator.parentNode = tagParent
            }
          })
        }
      } else {
        if (!_.isArray(indicator.tag_json) || indicator.tag_json.length === 0) {
          otherTag.children.push(indicator)
          indicator.parentNode = otherTag
        } else if (_.isArray(indicator.tag_json)) {
          indicator.tag_json.forEach(tId => {
            let tagParent = tags_map[tId]
            tagParent.children.push(indicator)
            indicator.parentNode = tagParent
          })
        }
      }
    })

    // add other tag?
    if (otherTag.children.length > 0) {
      sortTags.push(otherTag)
    }

    // sort indicators with each tag
    sortTags.forEach(tag => tag.children = _.sortBy(tag.children, 'title'))
    sortTags = treeify(sortTags, 'id')
    sortTags.reverse()

    if (isRemoveEmpty) {
      sortTags = this.removeIndicatorEmptyNode(sortTags)
    }

    return sortTags
  }
})

export default IndicatorStore
