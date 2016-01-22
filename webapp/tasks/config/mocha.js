import gulp from 'gulp'

export default {
  src: [
    `${gulp.config('base.src')}/**/__tests__/*.spec.js{,x}`
  ],
  options: {
    r: 'src/helpers/jsdom.js',
    R: 'dot',
    compilers: '.:babel/register',
    istanbul: true
  }
}
