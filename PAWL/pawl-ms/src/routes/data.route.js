const express = require('express')
const Measurement = require('../models/measurement.model')

const router = new express.Router()

router.get('/:identifier', async (req, res) => {
  const { identifier } = req.params
  const data = await Measurement.findOne({ identifier })
  const points = data.raw.split('_').map((item) => {
    const point = item.split('|')
    return {
      x: Number(point[0]),
      y: Number(point[1])
    }
  })
  res.status(201).send(points)
})

module.exports = router
