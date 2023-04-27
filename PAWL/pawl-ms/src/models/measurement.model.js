const mongoose = require('mongoose')

const measurementSchema = new mongoose.Schema({
  identifier: {
    type: String,
    required: true,
    trim: true
  },
  deviceId: {
    type: String,
    required: true,
    trim: true
  },
  raw: {
    type: String,
    required: true,
    trim: true
  }
}, {
  timestamps: true
})

const Measurement = mongoose.model('Measurement', measurementSchema)

module.exports = Measurement
