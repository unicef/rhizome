'use strict';

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _lodash = require('lodash');

var _lodash2 = _interopRequireDefault(_lodash);

var _reactAddons = require('react/addons');

var _reactAddons2 = _interopRequireDefault(_reactAddons);

var _classnames = require('classnames');

var _classnames2 = _interopRequireDefault(_classnames);

var _InterfaceMixin = require('./../InterfaceMixin');

var _InterfaceMixin2 = _interopRequireDefault(_InterfaceMixin);

var Paginator = _reactAddons2['default'].createClass({
    displayName: 'Paginator',

    mixins: [(0, _InterfaceMixin2['default'])('Datascope', 'DatascopePagination')],

    getDefaultProps: function getDefaultProps() {
        return {
            canHide: true,
            truncateLimit: 5,
            truncatedSize: 3,
            showPreviousNext: true,
            nextLabel: '>',
            previousLabel: '<'
        };
    },

    onClickPage: function onClickPage(page) {
        var offset = this.props.pagination.limit * (page - 1);
        var pagination = _lodash2['default'].extend({}, this.props.pagination, { offset: offset, page: page });
        this.props.onChangePagination(pagination);
    },

    render: function render() {
        var _this = this;

        if (!this.props.pagination) return null;
        var _props = this.props;
        var pagination = _props.pagination;
        var truncateLimit = _props.truncateLimit;
        var truncatedSize = _props.truncatedSize;

        var shouldHide = this.props.canHide && pagination.total < pagination.limit;
        if (shouldHide) return null;

        var minResult = pagination.offset + 1;
        var maxResult = Math.min(pagination.total, pagination.offset + pagination.limit);
        var thisPage = pagination.page;
        var lastPage = Math.ceil(pagination.total / pagination.limit);
        var nextPage = Math.min(thisPage + 1, lastPage);
        var previousPage = Math.max(thisPage - 1, 1);

        var pageNums = _lodash2['default'].range(1, lastPage + 1);
        var shouldTruncate = truncateLimit && lastPage > truncateLimit;

        if (shouldTruncate) {
            pageNums = (0, _lodash2['default'])([_lodash2['default'].range(1, truncatedSize + 1), // first few
            _lodash2['default'].range(lastPage - truncatedSize + 1, lastPage + 1), // last few
            [previousPage, thisPage, nextPage] // this page and its neighbors
            ]).flatten().uniq().value().sort(function (a, b) {
                return a - b;
            }); // mash em all together, dedupe and sort

            pageNums = _lodash2['default'].reduce(pageNums, function (result, page) {
                // insert '...' between breaks
                if (page > _lodash2['default'].last(result) + 1) result.push('...');
                result.push(page);
                return result;
            }, []);
        }

        return _reactAddons2['default'].createElement(
            'div',
            { className: 'datascope-paginator' },
            this.props.previousLabel && thisPage != 1 ? _reactAddons2['default'].createElement(
                'span',
                {
                    className: 'page-link page-link-previous',
                    onClick: _lodash2['default'].partial(this.onClickPage, previousPage)
                },
                this.props.previousLabel
            ) : '',
            pageNums.map(function (page) {
                return _lodash2['default'].isString(page) ? _reactAddons2['default'].createElement(
                    'span',
                    { className: 'pagination-truncate' },
                    page
                ) : _reactAddons2['default'].createElement(
                    'span',
                    {
                        className: (0, _classnames2['default'])('page-link', { active: page === thisPage }),
                        key: 'page' + page,
                        onClick: _this.onClickPage.bind(null, page)
                    },
                    page
                );
            }),
            this.props.nextLabel && thisPage != lastPage ? _reactAddons2['default'].createElement(
                'span',
                {
                    className: 'page-link page-link-next',
                    onClick: _lodash2['default'].partial(this.onClickPage, nextPage)
                },
                this.props.nextLabel
            ) : '',
            _reactAddons2['default'].createElement(
                'div',
                { className: 'pagination-count' },
                minResult,
                ' to ',
                maxResult,
                ' of ',
                pagination.total
            )
        );
    }
});

function offsetFromPage() {}

module.exports = Paginator;
