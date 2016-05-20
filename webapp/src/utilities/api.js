/* jshint browser: true */
/* global Promise */
const BASE_URL = '/api'

import _ from 'lodash'
import moment from 'moment'
import request from 'superagent'
import superagentPrefix from 'superagent-prefix'
const prefix = superagentPrefix(BASE_URL)

import treeify from 'utilities/transform/treeify'

function urlencode (query) {
  return '?' + _.map(query, function (v, k) {
    return encodeURIComponent(k) + '=' + encodeURIComponent(v)
  }).join('&')
}

function getCookie (name) {
  var cookieValue = null
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split('')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i] // jQuery.trim(cookies[i])
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

function emptyResponsePoint (path, mode, defaultVersion, useDefaults) {
  mode = (mode) ? mode.toUpperCase() : 'GET'
  defaultVersion = defaultVersion || 1
  useDefaults = _.isUndefined(useDefaults) ? true : useDefaults

  var defaults = {
    format: 'json'
  }

  function fetch (query, version, headers) {
    version = version || defaultVersion
    headers = headers || {}

    var versionedPath = '/v' + version + path
    var req = prefix(request(mode, versionedPath))

    if (mode === 'GET' || mode === 'DELETE') {
      var q = useDefaults ? _.defaults({}, query, defaults) : query
      req.query(q)
        .set(headers)
        .send()
    } else if (mode === 'POST' || mode === 'PATCH') {
      var csrftoken = getCookie('csrftoken')
      req.query(defaults)
        .set('X-CSRFToken', csrftoken)
        .set('Content-Type', 'application/x-www-form-urlencoded')
        .send(query)
    }

    return new Promise(function (fulfill, reject) {
      req.end(function (error, res) {
        if (error) {
          reject({
            status: res.status,
            msg: ''
          })
        } else {
          fulfill({
            meta: {},
            objects: null
          })
        }
      })
    })
  }

  fetch.toString = function (query, version) {
    version = version || defaultVersion
    var versionedPath = '/v' + version + path

    return BASE_URL + versionedPath + urlencode(_.defaults({}, query, defaults))
  }

  return fetch
}

function endPoint (path, mode, defaultVersion, useDefaults) {
  mode = mode ? mode.toUpperCase() : 'GET'
  defaultVersion = defaultVersion || 1
  useDefaults = _.isUndefined(useDefaults) ? true : useDefaults

  var defaults = {
    format: 'json'
  }

  function fetch (query, version, headers) {
    version = version || defaultVersion
    headers = headers || {}

    var versionedPath = '/v' + version + path
    var req = prefix(request(mode, versionedPath))

    if (mode === 'GET' || mode === 'DELETE') {
      var q = useDefaults ? _.defaults({}, query, defaults) : query
      req.query(q)
        .set(headers)
        .send()
    } else if (mode === 'POST' || mode === 'PATCH') {
      var csrftoken = getCookie('csrftoken')
      req.query(defaults)
        .set('X-CSRFToken', csrftoken)
        .set('Content-Type', 'application/x-www-form-urlencoded')
        .send(query)
    }

    return new Promise(function (fulfill, reject) {
      req.end(function (err, res) {
        if (err) {
          reject({
            status: res.status,
            msg: res.body ? res.body.error : '',
            code: res.body ? res.body.code : -1
          })
        } else if (!res.body) {
          fulfill(res)
        } else {
          fulfill({
            meta: res.body.meta || {},
            objects: _.isArray(res.body)
              ? res.body
              : res.body.objects || _.omit(res.body, 'meta')
          })
        }
      })
    })
  }

  fetch.toString = function (query, version) {
    version = version || defaultVersion
    var versionedPath = '/v' + version + path

    return BASE_URL + versionedPath + urlencode(_.defaults({}, query, defaults))
  }

  return fetch
}

function submissionDownload (document_id) {
  var fetch = endPoint('/source_submission/', null, null, true)
  return new Promise(function (fulfill, reject) {
    fetch({'document_id': document_id, 'format': 'csv'}, null, {'cache-control': 'no-cache'}).then(function (data) {
      fulfill(data)
    }, reject)
  })
}

function datapoint (q) {
  var fetch = endPoint('/datapoint/')

  return new Promise(function (fulfill, reject) {
    // needs to be cleaned up -- previously this method called the campaign api
    fetch(q, null, {'cache-control': 'no-cache'}).then(function (data) {
      var campaignData = data.meta.campaign_list
      var campaignIx = _.indexBy(campaignData, 'id')
      for (var i = data.objects.length - 1; i >= 0; --i) {
        data.objects[i].campaign = setCampaign(campaignIx[data.objects[i].campaign])
      }
      fulfill(data)
    }, reject)
  })
}

datapoint.toString = function (query, version) {
  return endPoint('/datapoint/').toString(query, version)
}

function setCampaign (obj) {
  return obj
    ? update({}, obj)
    : {
      id: null,
      created_at: null,
      start_date: null,
      end_date: null,
      name: null,
      slug: null,
      resource_uri: null
    }
}

function update (campaign, obj) {
  _.assign(campaign, _.omit(obj, 'created_at', 'start_date', 'end_date'))
  campaign.created_at = moment(obj.created_at).toDate()
  campaign.start_date = moment(obj.start_date, 'YYYY-MM-DD').toDate()
  campaign.end_date = moment(obj.end_date, 'YYYY-MM-DD').toDate()
  return campaign
}

function makeTagId (tId) {
  return 'tag-' + tId
}

function pickAllNodesInTrees (parent, nodes) {
  let children = parent.children

  if (children && children.length) {
    children.forEach(item => pickAllNodesInTrees(item, nodes))
  } else {
    if (parent.noValue) nodes.push(parent)
  }
}

function removeIndicatorEmptyNode (sourceList) {
  if (!sourceList || !sourceList.length) {
    return sourceList
  }

  let virtualRoot = {noValue: false, parentNode: null, title: 'No Available Indicator', children: sourceList}
  virtualRoot.children.forEach(item => item.parentNode = virtualRoot)

  let nodes
  do {
    nodes = []
    pickAllNodesInTrees(virtualRoot, nodes)
    nodes.forEach(function (item) {
      item.parentNode.children.splice(item.parentNode.children.indexOf(item), 1)
    })
  } while (nodes.length > 0)

  if (sourceList.length > 0) {
    return sourceList
  } else {
    virtualRoot.noValue = true
    virtualRoot.children = []
    return [virtualRoot]
  }
}

function buildIndicatorsTree (indicators, tags, isClone, isRemoveEmpty, indicatorFilterType) {
  if (isClone) {
    tags = _.cloneDeep(tags)
    indicators = _.cloneDeep(indicators)
  }

  let sortTags = _.sortBy(tags, 'tag_name').reverse()

  var tags_map = {}
  _.each(sortTags, function (t) {
    tags_map[t.id] = t
    t.id = makeTagId(t.id)
    t.noValue = true
    t.parent = t.parent_tag_id && t.parent_tag_id !== 'None' ? makeTagId(t.parent_tag_id) : null
    t.children = []
    t.title = t.tag_name
    t.value = t.id
  })

  // add 'Other Indicators' tag to collect any indicators without tags
  var otherTag = {
    'id': 0,
    'value': makeTagId(0),
    'noValue': true,
    'title': 'Other Indicators',
    'children': []
  }

  _.each(indicators, function (i) {
    i.title = i.name
    i.value = i.id
    i.displayTitle = i.name + ' (' + i.id + ')'
    if (indicatorFilterType) {
      if (!_.isArray(i.tag_json) || i.tag_json.length === 0) {
        if (indicatorFilterType && i.data_format === indicatorFilterType) {
          otherTag.children.push(i)
          i.parentNode = otherTag
        }
      } else if (_.isArray(i.tag_json)) {
        _.each(i.tag_json, function (tId) {
          if (indicatorFilterType && i.data_format === indicatorFilterType) {
            let tagParent = tags_map[tId]
            tagParent.children.push(i)
            i.parentNode = tagParent
          }
        })
      }
    } else {
      if (!_.isArray(i.tag_json) || i.tag_json.length === 0) {
        otherTag.children.push(i)
        i.parentNode = otherTag
      } else if (_.isArray(i.tag_json)) {
        _.each(i.tag_json, function (tId) {
          let tagParent = tags_map[tId]
          tagParent.children.push(i)
          i.parentNode = tagParent
        })
      }
    }
  })

  // add other tag?
  if (otherTag.children.length > 0) {
    sortTags.push(otherTag)
  }
  // tags.objects.reverse()
  // sort indicators with each tag
  _.each(sortTags, function (t) {
    t.children = _.sortBy(t.children, 'title')
  })

  sortTags = treeify(sortTags, 'id')
  sortTags.reverse()

  if (isRemoveEmpty) {
    sortTags = removeIndicatorEmptyNode(sortTags)
  }

  return sortTags
}

function indicatorsTree (q) {
  var fetch1 = endPoint('/indicator/', 'get', 1)
  var fetch2 = endPoint('/indicator_tag/', 'get', 1)
  return new Promise(function (fulfill, reject) {
    fetch1(q, null, {'cache-control': 'no-cache'}).then(function (indicators) {
      fetch2(null, null, {'cache-control': 'no-cache'}).then(function (tags) {
        let tree = buildIndicatorsTree(indicators.objects, tags.objects, false, true)
        tags.rawTags = tags.objects
        tags.objects = tree
        tags.flat = indicators.objects
        fulfill(tags)
      })
    }, reject)
  })
}

function tagTree (q) {
  var fetch = endPoint('/indicator_tag/', 'get', 1)
  return new Promise(function (fulfill, reject) {
    fetch().then(function (tags) {
      var tags_map = {}
      _.each(tags.objects, function (t) {
        tags_map[t.id] = t
        t.parent = t.parent_tag_id
        t.children = []
        t.title = t.tag_name
        t.value = t.id
      })
      tags.objects = treeify(tags.objects, 'id')
      tags.flat = tags.objects
      fulfill(tags)
    }, reject)
  })
}

export default {
  endPoint,
  // CUSTOM GET REQUESTS -> MANIPULATED BY JS //
  datapoints: datapoint,
  submissionDownload: submissionDownload,
  indicatorsTree: indicatorsTree,
  tagTree: tagTree,
  buildIndicatorsTree: buildIndicatorsTree,

  // BASIC GET REQUESTS //
  campaign: endPoint('/campaign/', 'get', 1),
  campaign_type: endPoint('/campaign_type/', 'get', 1),
  locations: endPoint('/location/', 'get', 1),
  datapointsRaw: endPoint('/datapointentry/', 'get', 1),
  indicators: endPoint('/indicator/', 'get', 1),
  office: endPoint('/office/', 'get', 1),
  homepage: endPoint('/homepage/', 'get', 1),
  location_type: endPoint('/location_type/', 'get', 1),
  post_indicator: endPoint('/indicator/', 'post', 1),
  indicator_to_calc: endPoint('/indicator_calculation/', 'get', 1),
  remove_calc_from_indicator: emptyResponsePoint('/indicator_calculation', 'delete', 1, false),
  set_calc_to_indicator: endPoint('/indicator_calculation/', 'post', 1),

  indicator_to_tag: endPoint('/indicator_to_tag/', 'get', 1),
  get_indicator_tag: endPoint('/indicator_tag/', 'get', 1),
  post_indicator_tag: endPoint('/indicator_tag/', 'post', 1),
  get_dashboard: endPoint('/custom_dashboard/', 'get', 1),
  get_chart: endPoint('/custom_chart/', 'get', 1),
  get_all_meta: endPoint('/all_meta/', 'get', 1),
  post_chart: endPoint('/custom_chart/', 'post', 1),
  post_dashboard: endPoint('/custom_dashboard/', 'post', 1),
  delete_chart: emptyResponsePoint('/custom_chart', 'delete', 1, false),
  groups: endPoint('/group/', 'get', 1),
  users: endPoint('/user/', 'get', 1),
  location_responsibility: endPoint('/location_responsibility/', 'get', 1),
  geo: endPoint('/geo/', 'get', 1),
  get_source_object_map: endPoint('/source_object_map/', 'get', 1),
  user_permissions: endPoint('/user_group/', 'get', 1),
  post_user_permission: endPoint('/user_group/', 'post', 1),
  delete_user_permission: emptyResponsePoint('/user_group', 'delete', 1, false),

  sync_odk: endPoint('/sync_odk/', 'get', 1, false),
  refresh_master: endPoint('/refresh_master/', 'get', 1, false),
  queue_reprocess: endPoint('/queue_process/', 'get', 1, false),
  chartType: endPoint('/chart_type/', 'get', 1),

  // SOURCE DATA DASHBOARD REQUESTS //
  source_doc: endPoint('/source_doc/', 'get', 1),
  submission: endPoint('/source_submission/', 'get', 1, false),
  docDetail: endPoint('/doc_detail/', 'get', 1, false),
  docMapped: endPoint('/source_object_map/', 'get', 1, false),
  docDatapoint: endPoint('/doc_datapoint/', 'get', 1, false),
  docResults: endPoint('/computed_datapoint/', 'get', 1, false),
  docDetailType: endPoint('/doc_detail_type/', 'get', 1, false),
  transformUpload: endPoint('/transform_upload/', 'get', 1, false),

  // POST //
  docDetailPost: endPoint('/doc_detail/', 'post'),
  uploadPost: endPoint('/source_doc/', 'post'),
  datapointUpsert: endPoint('/datapointentry/', 'post'),
  save_dashboard: endPoint('/custom_dashboard/', 'post', 1),
  post_campaign: endPoint('/campaign/', 'post', 1),
  remove_dashboard: emptyResponsePoint('/custom_dashboard', 'delete', 1, false),
  set_location_responsibility: endPoint('/location_responsibility/', 'post', 1),
  delete_location_responsibility: emptyResponsePoint('/location_responsibility', 'delete', 1, false),
  remove_indicator_from_tag: emptyResponsePoint('/indicator_to_tag', 'delete', 1, false),
  set_indicator_to_tag: endPoint('/indicator_to_tag/', 'post', 1),
  post_source_object_map: endPoint('/source_object_map/', 'post', 1, false)
}
