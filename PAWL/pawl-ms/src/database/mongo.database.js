const mongoose = require('mongoose')
const config = require('config')
const log = require('../services/logger.service')

const host = config.get('mongoose.host')
const port = config.get('mongoose.port')
const database = config.get('mongoose.database')
const options = {
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000
}

mongoose.connect(`mongodb://${host}:${port}/${database}`, options)
mongoose.connection.on('reconnected', () => {
  log.warn('Mongoose reconnected to database')
})
mongoose.connection.on('connected', () => {
  log.info('Mongoose connected to database')
})
mongoose.connection.on('disconnected', () => {
  log.error('Mongoose connection error: disconnected')
})
mongoose.connection.on('error', (error) => {
  log.error(`Mongoose connection error: ${error.message}`)
})
