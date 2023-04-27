const express = require('express')
const log = require('../services/logger.service')
const Measurement = require('../models/measurement.model')

const router = new express.Router()

router.post('/', async (req, res) => {
  log.info('POST /pawl/v1/api/measurement')
  const { body } = req
  const measurement = new Measurement(body)
  try {
    await measurement.save()
    res.status(201).send(measurement)
  } catch (error) {
    log.error(error)
    res.status(400).send(error)
  }
})

router.delete('/', async (req, res) => {
  log.info('DELETE /pawl/v1/api/measurement')
  try {
    await Measurement.deleteMany()
    res.status(200).send()
  } catch (error) {
    log.error(error)
    res.status(500).send(error)
  }
})

module.exports = router
