const prod = process.env.NODE_ENV === 'production'
module.exports = {
  pluginOptions: {
    s3Deploy: {
      registry: undefined,
      awsProfile: 'default',
      region: 'us-east-2',
      bucket: 'static-vue-bucket',
      createBucket: true,
      staticHosting: true,
      staticIndexPage: 'index.html',
      staticErrorPage: 'index.html',
      assetPath: 'dist',
      assetMatch: '**',
      deployPath: '/',
      acl: 'public-read',
      pwa: false,
      enableCloudfront: false,
      uploadConcurrency: 5,
      pluginVersion: '3.0.0'
    }
  },
  baseUrl: prod ? '/static-vue-bucket/' : '/'
}
