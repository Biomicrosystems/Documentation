using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MeasureLibrary
{
    /// <summary>
    /// Measurement Class XD
    /// </summary>
    public class Measure
    {
        private double calculateMagnitude()
        {
            return Math.Sqrt(Math.Pow(_Horizontal, 2) + Math.Pow(_Vertical, 2));
        }

        private int _StartX;
        /// <summary>
        /// Starting point X Value
        /// </summary>
        public int StartX
        {
            get { return _StartX; }
            set
            {
                _StartX = value;
                _Horizontal = _EndX - _StartX;
            }
        }

        private int _StartY;
        /// <summary>
        /// Starting point Y Value
        /// </summary>
        public int StartY
        {
            get { return _StartY; }
            set
            {
                _StartY = value;
                _Vertical = _EndY - _StartY;
            }
        }

        private int _EndX;
        /// <summary>
        /// Final point X Value
        /// </summary>
        public int EndX
        {
            get { return _EndX; }
            set
            {
                _EndX = value;
                _Horizontal = _EndX - _StartX;
            }
        }

        private int _EndY;
        /// <summary>
        /// Final point Y Value
        /// </summary>
        public int EndY
        {
            get { return _EndY; }
            set
            {
                _EndY = value;
                _Vertical = _EndY - _StartY;
            }
        }

        private int _Horizontal;
        /// <summary>
        /// Horizontal Value
        /// </summary>
        public int Horizontal
        {
            get { return _Horizontal; }
        }

        private int _Vertical;
        /// <summary>
        /// Vertical Value
        /// </summary>
        public int Vertical
        {
            get { return _Vertical; }
            set { _Vertical = value; }
        }

        private double _Magnitude;
        /// <summary>
        /// Magnitude Value
        /// </summary>
        public double Magnitude
        {
            get
            {
                _Magnitude = calculateMagnitude();
                return _Magnitude;
            }
            set { _Magnitude = value; }
        }


        private double _Angle;
        /// <summary>
        /// Angle Value
        /// </summary>
        public double Angle
        {
            get { return _Angle; }
            set { _Angle = value; }
        }

    }
}
