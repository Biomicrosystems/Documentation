using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;

namespace MeasureLibrary
{
    public partial class Measure_Template : UserControl
    {
        private Measure _Measures = new Measure();
        private bool isMeasuring = false;
        private int pointCount = 0;

        public Measure Measures
        {
            get { return _Measures; }
            set { _Measures = value; }
        }

        public Measure_Template()
        {
            InitializeComponent();
        }

        private void Measure_Template_Load(object sender, EventArgs e)
        {
            pbxMeasureImage.AllowDrop = true;
        }

        private void pbxMeasureImage_DragEnter(object sender, DragEventArgs e)
        {
            e.Effect = DragDropEffects.Copy;
        }

        private bool GetFilename(out string filename, DragEventArgs e)
        {
            bool ret = false;
            filename = String.Empty;

            if ((e.AllowedEffect & DragDropEffects.Copy) == DragDropEffects.Copy)
            {
                Array data = ((IDataObject)e.Data).GetData("FileName") as Array;
                if (data != null)
                {
                    if ((data.Length == 1) && (data.GetValue(0) is String))
                    {
                        filename = ((string[])data)[0];
                        string ext = Path.GetExtension(filename).ToLower();
                        if ((ext == ".jpg") || (ext == ".png") || (ext == ".bmp"))
                        {
                            ret = true;
                        }
                    }
                }
            }
            return ret;
        }

        private void pbxMeasureImage_DragDrop(object sender, DragEventArgs e)
        {

            string filename;
            var validData = GetFilename(out filename, e);
            if (validData)
            {
                if (filename != null)
                {
                    pbxMeasureImage.Image = Image.FromFile(filename);
                }
            }
        }

        private void btn_Measure_Click(object sender, EventArgs e)
        {
            isMeasuring = true;
            pointCount = 0;
        }

        private void pbxMeasureImage_MouseClick(object sender, MouseEventArgs e)
        {
            try
            {
                if (isMeasuring)
                {
                    switch (pointCount++)
                    {
                        case 0: //Clic inicial
                            Measures.StartX = e.X * (pbxMeasureImage.Image.Width) / (pbxMeasureImage.Width);
                            Measures.StartY = pbxMeasureImage.Image.Height - e.Y * (pbxMeasureImage.Image.Height) / (pbxMeasureImage.Height);
                            break;
                        case 1: //Clic Final
                            Measures.EndX = e.X * (pbxMeasureImage.Image.Width) / (pbxMeasureImage.Width);
                            Measures.EndY = pbxMeasureImage.Image.Height - e.Y * (pbxMeasureImage.Image.Height) / (pbxMeasureImage.Height);

                            isMeasuring = false;
                            pointCount = 0;
                            break;
                        default:
                            break;
                    }
                    UpdateControls();
                }
            }
            catch (Exception ex)
            {
                isMeasuring = false;
                pointCount = 0;
            }
        }

        private void UpdateControls()
        {
            nStartX.Value = Measures.StartX;
            nStartY.Value = Measures.StartY;

            nEndX.Value = Measures.EndX;
            nEndY.Value = Measures.EndY;

            txtHorizontal.Text = "" + Math.Abs(Measures.Horizontal);
            txtVertical.Text = "" + Math.Abs(Measures.Vertical);
            txtMagnitude.Text = "" + Measures.Magnitude;
            txtAngle.Text = "" + Measures.Angle;
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}
