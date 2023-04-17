const express = require('express')
const config = require('config')
const cors = require('cors')
const log = require('./src/services/logger.service')

const app = express()
const port = config.get('server.port')
const host = config.get('server.host')
const router = require('./src/routes/router')
require('./src/database/mongo.database')

app.use(cors()).use(express.json()).use(router)
app.listen(port, () => {
  log.info(`PAWL API listening at https://${host}:${port}`)
})

module.exports = app
