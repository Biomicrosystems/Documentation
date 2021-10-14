using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Drawing.Imaging;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;

namespace MeasureLibrary
{
    public partial class MeasureWindow : UserControl
    {
        private Bitmap Orig, ZOrig;
        private bool isClicked = false;
        private Rectangle section;
        private Measure _Measures = new Measure();
        private bool isMeasuring;
        private int pointCount;

        public Measure Measures
        {
            get { return _Measures; }
            set { _Measures = value; }
        }

        public MeasureWindow()
        {
            InitializeComponent();
            foreach (Control item in Controls)
                if (item is ComboBox)
                    if (((ComboBox)item).Items.Count > 0)
                        ((ComboBox)item).SelectedIndex = 0;
        }

        private void MeasureWindow_Load(object sender, EventArgs e)
        {
            pbxBigImage.AllowDrop = true;
        }

        private void pbxBigImage_DragEnter(object sender, DragEventArgs e)
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

        private void pbxBigImage_DragDrop(object sender, DragEventArgs e)
        {
            string filename;
            var validData = GetFilename(out filename, e);
            if (validData)
            {
                if (filename != null)
                {
                    Orig = (Bitmap)Image.FromFile(filename);
                    pbxBigImage.Image = (Bitmap)Orig.Clone();
                }
            }
        }

        private void pbxBigImage_MouseUp(object sender, MouseEventArgs e)
        {
            isClicked = false;
            Cursor = Cursors.Default;
        }

        private void pbxBigImage_MouseDown(object sender, MouseEventArgs e)
        {
            if (pbxBigImage.Image != null)
            {
                isClicked = true;
                section = getRectangle(e.X, e.Y, cropSize);
                ZOrig = ((Bitmap)Orig).Clone(section, ((Bitmap)Orig).PixelFormat);
                pbxZoomImage.Image = (Bitmap)ZOrig.Clone();
                pbxZoomImage.Refresh();
                pbxBigImage.Refresh();
                Cursor = Cursors.Cross;
            }
            else
            {
                Cursor = Cursors.Default;
                isClicked = false;
            }
        }

        private Rectangle getRectangle(int x, int y, int width)
        {
            int midWidth = width / 2;

            int _localX = ((x * pbxBigImage.Image.Width) / pbxBigImage.Width) - midWidth;
            int _localY = ((y * pbxBigImage.Image.Height) / pbxBigImage.Height) - midWidth;
            if (_localX <= 0)
                _localX = 0;
            if (_localX >= pbxBigImage.Image.Width - width)
                _localX = pbxBigImage.Image.Width - width;
            if (_localY <= 0)
                _localY = 0;
            if (_localY >= pbxBigImage.Image.Height - width)
                _localY = pbxBigImage.Image.Height - width;
            Rectangle rec = new Rectangle(new Point(_localX, _localY), new Size(width, width));
            Bitmap tmp = (Bitmap)Orig.Clone();
            return rec;
        }
        public int cropSize = 200;
        private void pbxBigImage_MouseMove(object sender, MouseEventArgs e)
        {
            if (isClicked)
            {
                section = getRectangle(e.X, e.Y, cropSize);
                ZOrig = ((Bitmap)Orig).Clone(section, ((Bitmap)Orig).PixelFormat);
                pbxZoomImage.Image = (Bitmap)ZOrig.Clone();
                pbxZoomImage.Refresh();
                pbxBigImage.Refresh();
                Cursor = Cursors.Cross;
            }
            else
            {
                Cursor = Cursors.Default;
            }
        }

        private void btn_measure_Click(object sender, EventArgs e)
        {
            isMeasuring = true;
            pointCount = 0;
            updateBar();
        }

        private void updateBar()
        {
            try
            {
                if (pbxZoomImage.Image != null)
                {
                    pbxZoomImage.Image = (Bitmap)ZOrig.Clone();
                    using (Graphics g = Graphics.FromImage(pbxZoomImage.Image))
                    {
                        int yt = (int)(cropSize * 0.93);
                        int scalex = 0;
                        String txt = "";
                        switch (comboBox1.SelectedItem.ToString())
                        {
                            case "mm":
                                scalex = (int)(double.Parse(txtScale.Text) * 1000);
                                break;
                            case "um":
                                scalex = (int)(double.Parse(txtScale.Text));
                                break;
                            case "nm":
                                scalex = (int)(double.Parse(txtScale.Text) / 1000);
                                break;
                            default:
                                break;
                        }
                        int xm = (int)(scalex * double.Parse(txt_pixels.Text) / double.Parse(txtDist.Text));
                        g.DrawLine(new Pen(Color.Black, cropSize / 30), yt - xm, yt, yt, yt);


                        txt = txtScale.Text;
                        txt += comboBox1.SelectedItem.ToString();
                        g.DrawString(txt, new Font(FontFamily.GenericSansSerif, cropSize / 50),
                            new SolidBrush(Color.Black), cropSize / 3, (int)(cropSize * 0.8));
                        // g.DrawRectangle(new Pen(Color.Red, 10), new Rectangle(new Point(x, y), new Size(width, width)));
                    }
                }
            }
            catch (Exception ex)
            {
            }
        }

        private void pbxZoomImage_MouseClick(object sender, MouseEventArgs e)
        {
            try
            {
                if (isMeasuring)
                {
                    switch (pointCount++)
                    {
                        case 0: //Clic inicial
                            Measures.StartX = e.X * (pbxZoomImage.Image.Width) / (pbxZoomImage.Width);
                            Measures.StartY = pbxZoomImage.Image.Height - e.Y * (pbxZoomImage.Image.Height) / (pbxZoomImage.Height);
                            break;
                        case 1: //Clic Final
                            Measures.EndX = e.X * (pbxZoomImage.Image.Width) / (pbxZoomImage.Width);
                            Measures.EndY = pbxZoomImage.Image.Height - e.Y * (pbxZoomImage.Image.Height) / (pbxZoomImage.Height);

                            isMeasuring = false;
                            pointCount = 0;
                            UpdateControls();
                            break;
                        default:
                            break;
                    }

                }
            }
            catch (Exception ex)
            {
                isMeasuring = false;
                pointCount = 0;
            }
        }

        private void pbxZoomImage_MouseLeave(object sender, EventArgs e)
        {
            if (isMeasuring)
            {
                Cursor = Cursors.Default;
            }
        }

        private void pbxZoomImage_MouseEnter(object sender, EventArgs e)
        {
            if (isMeasuring)
            {
                Cursor = Cursors.Cross;
            }
        }

        private void btn_save_Click(object sender, EventArgs e)
        {
            try
            {
                if (pbxZoomImage.Image != null)
                {
                    saveFileDialog1.FileName = "" + DateTime.Now.ToString("dd-MM-yyyy") + " " + txt_final.Text + ".jpg";
                    saveFileDialog1.DefaultExt = "jpg";
                    saveFileDialog1.Filter = "JPG images (*.jpg)|*.jpg";
                    if (saveFileDialog1.ShowDialog(this) == DialogResult.OK)
                    {
                        Bitmap bmp = (Bitmap)pbxZoomImage.Image;
                        bmp.Save(saveFileDialog1.FileName, ImageFormat.Jpeg);
                        bmp.Dispose();
                    }
                }
            }
            catch (Exception ex)
            {

            }
        }

        private void size100x100ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            cropSize = 100;
        }

        private void size200x200ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            cropSize = 200;
        }

        private void size300x300ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            cropSize = 400;
        }

        private void size400x400ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            cropSize = 600;
        }

        private void UpdateControls()
        {
            double measure = (Measures.Magnitude / int.Parse(txt_pixels.Text)) * double.Parse(txtDist.Text);
            txt_final.Text = String.Format("{0:0.0000}" + comboBox2.SelectedItem.ToString(), measure);
        }
    }
}
