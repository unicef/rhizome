import _ from 'lodash'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'
import IndicatorActions from 'actions/IndicatorActions'
import treeify from 'utilities/transform/treeify'

var IndicatorStore = Reflux.createStore({

  mixins: [StateMixin.store],

  listenables: IndicatorActions,

  indicators: {
    meta: null,
    raw: null,
    index: null,
    filtered: [],
    list: [],
    tree: []
  },

  getInitialState: function () {
    return this.indicators
  },

  // =========================================================================== //
  //                              API CALL HANDLERS                              //
  // =========================================================================== //

  // ============================  Fetch Indicators  =========================== //
  onFetchIndicators: function () {
    this.setState({ raw: [] })
  },
  onFetchIndicatorsCompleted: function (response) {
    this.indicators.meta = response.meta
    this.indicators.raw = response.objects[0].indicators || response.objects
    this.indicators.filtered = this.indicators.raw
    this.indicators.index = _.indexBy(this.indicators.raw, 'id')
    this.processIndicators()
  },
  onFetchIndicatorsFailed: function (error) {
    this.setState({ error: error })
  },

  // ===========================  Fetch Indicator Tags ========================= //
  onFetchIndicatorTags: function () {
    this.setState({ raw: [] })
  },
  onFetchIndicatorTagsCompleted: function (response) {
    this.indicators.tags = response.objects[0].indicator_tags || response.objects
    this.processIndicators()
  },
  onFetchIndicatorTagsFailed: function (error) {
    this.setState({ error: error })
  },

  // ===========================  Fetch IndicatorsToTags ========================= //
  onFetchIndicatorsToTags: function () {
    this.setState({ raw: [] })
  },
  onFetchIndicatorsToTagsCompleted: function (response) {
    const grouped_indicators_to_tags = _.groupBy(response.objects[0].indicators_to_tags, 'indicator_tag_id')
    this.indicators.tags.forEach(tag => {
      tag.indicators = _.map(grouped_indicators_to_tags[tag.id], indicator_to_tag => {
        return this.indicators.index[indicator_to_tag.indicator_id]
      })
    })
    this.processIndicators()
  },
  onFetchIndicatorsToTagsFailed: function (error) {
    this.setState({ error: error })
  },

  // =========================================================================== //
  //                                   UTILITIES                                 //
  // =========================================================================== //
  processIndicators: function () {
    if (this.indicators.raw && this.indicators.tags) {
      this.indicators.tree = this.buildIndicatorsTree(this.indicators.raw, this.indicators.tags, true, true)
      this.indicators.list = _.sortBy(this.indicators.tree, 'title')
      this.trigger(this.indicators)
    }
  },

  makeTagId: function (tId) {
    return 'tag-' + tId
  },

  pickAllNodesInTrees: function (parent, nodes) {
    let children = parent.children
    if (children && children.length) {
      children.forEach(item => this.pickAllNodesInTrees(item, nodes))
    } else {
      if (parent.noValue) nodes.push(parent)
    }
  },

  removeIndicatorEmptyNode: function (sourceList) {
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

  buildIndicatorsTree: function (indicators, tags, isClone, isRemoveEmpty, indicatorFilterType) {
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
      indicator.parsed_tag_json = JSON.parse(indicator.tag_json)

      if (indicatorFilterType) {
        if (!_.isArray(indicator.tag_json) || indicator.tag_json.length === 0) {
          if (indicatorFilterType && indicator.data_format === indicatorFilterType) {
            otherTag.children.push(indicator)
            indicator.parentNode = otherTag
          }
        } else if (_.isArray(indicator.parsed_tag_json)) {
          indicator.parsed_tag_json.forEach(tId => {
            if (indicatorFilterType && indicator.data_format === indicatorFilterType) {
              let tagParent = tags_map[tId]
              tagParent.children.push(indicator)
              indicator.parentNode = tagParent
            }
          })
        }
      } else {
        if (!_.isArray(indicator.parsed_tag_json) || indicator.parsed_tag_json.length === 0) {
          otherTag.children.push(indicator)
          indicator.parentNode = otherTag
        } else if (_.isArray(indicator.parsed_tag_json)) {
          indicator.parsed_tag_json.forEach(tId => {
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
