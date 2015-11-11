import url from 'url'
import gulp from 'gulp'
import config from 'config'
import compress from 'compression'
import proxyMiddleware from 'proxy-middleware'

export default {
  src: [
    `${gulp.config('base.dist')}/{,**/}*.*'`
  ],
  options: {
    notify: false,
    logSnippet: false,
    snippetOptions: {
      rule: {
        match: /$/,
        fn: function () {
          return ''
        }
      }
    },
    server: {
      baseDir: `${gulp.config('base.dist')}`,
      middleware: [
        process.env.NODE_ENV === 'production' ? compress() : middlewareNope(),
        proxyTo('/api/v2', url.format(config.get('server')))
      ]
    },
    ui: {
      port: 9999
    }
  }
}

function middlewareNope () {
  return (req, res, next) => {
    return next()
  }
}

function proxyTo (route, remoteUrl) {
  const options = url.parse(remoteUrl)
  options.route = route
  return proxyMiddleware(options)
}
