const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
    css: {
        loaderOptions: {
            sass: {
                additionalData: `@use '~@/styles/base/_variables.scss' as *;`
            }
        }
    }
})
