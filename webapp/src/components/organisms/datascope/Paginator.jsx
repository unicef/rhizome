import _ from 'lodash'
import React from 'react/addons'
import classnames from 'classnames'
import InterfaceMixin from 'utilities/InterfaceMixin'

let Paginator = React.createClass({
  displayName: 'Paginator',

  mixins: [(0, InterfaceMixin)('Datascope', 'DatascopePagination')],

  propTypes: {
    onChangePagination: React.PropTypes.func,
    canHide: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      canHide: true,
      truncateLimit: 5,
      truncatedSize: 3,
      showPreviousNext: true,
      nextLabel: '>',
      previousLabel: '<'
    }
  },

  onClickPage: function (page) {
    let offset = this.props.pagination.limit * (page - 1)
    let pagination = _.extend({}, this.props.pagination, { offset: offset, page: page })
    this.props.onChangePagination(pagination)
  },

  render: function () {
    let _this = this

    if (!this.props.pagination) return null
    let _props = this.props
    let pagination = _props.pagination
    let truncateLimit = _props.truncateLimit
    let truncatedSize = _props.truncatedSize
    let shouldHide = this.props.canHide && pagination.total < pagination.limit
    if (shouldHide) return null

    let minResult = pagination.offset + 1
    let maxResult = Math.min(pagination.total, pagination.offset + pagination.limit)
    let thisPage = pagination.page
    let lastPage = Math.ceil(pagination.total / pagination.limit)
    let nextPage = Math.min(thisPage + 1, lastPage)
    let previousPage = Math.max(thisPage - 1, 1)
    let pageNums = _.range(1, lastPage + 1)
    let shouldTruncate = truncateLimit && lastPage > truncateLimit
    if (shouldTruncate) {
      pageNums = (0, _)([_.range(1, truncatedSize + 1), // first few
      _.range(lastPage - truncatedSize + 1, lastPage + 1), // last few
      [previousPage, thisPage, nextPage] // this page and its neighbors
      ]).flatten().uniq().value().sort(function (a, b) {
        return a - b
      }) // mash em all together, dedupe and sort

      pageNums = _.reduce(pageNums, function (result, page) {
        // insert '...' between breaks
        if (page > _.last(result) + 1) result.push('...')
        result.push(page)
        return result
      }, [])
    }
    let previousButton = this.props.previousLabel && thisPage != 1 ? <span className="page-link page-link-previous"
                                                                    onClick={_.partial(this.onClickPage, previousPage)}>
                                                                    {this.props.previousLabel}</span>
                                                                  : ''
    let pageNumbers = pageNums.map(page => {
        return _.isString(page) ? <span className='pagination-truncate'>{page}</span>
                                : <span className={(0, classnames)('page-link', { active: page === thisPage })}
                                        key={'page' + page}
                                        onClick={_this.onClickPage.bind(null, page)}>
                                    {page}
                                  </span>
                                })
    let nextButton = this.props.nextLabel && thisPage !== lastPage ? <span className='page-link page-link-next' onClick={_.partial(this.onClickPage, nextPage)}>
                                                                      {this.props.nextLabel}
                                                                     </span>
                                                                    : ''
    let paginationCountLabel = <div className='pagination-count'>
                                {minResult} to {maxResult} of {pagination.total}
                               </div>
    return (
        <div className="datascope-paginator">
          {previousButton}{pageNumbers}{nextButton}
        </div>
      )
  }
})

export default Paginator
