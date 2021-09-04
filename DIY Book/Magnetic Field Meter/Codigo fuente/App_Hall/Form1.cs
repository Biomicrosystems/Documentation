using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;
using System.Threading;

namespace App_Hall
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false;
            //this.Text = "" + (((180 * 5000 / 1024) - 2500) / 1.4 * 0.1);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                if (serialPort1.IsOpen)
                    serialPort1.Close();

                serialPort1.PortName = comboBox1.SelectedItem.ToString();

                serialPort1.Open();
                timer1.Start();
            }
            catch (Exception ex)
            {
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            var s = SerialPort.GetPortNames();
            foreach (String r in s)
            {
                comboBox1.Items.Add(r);
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                serialPort1.Write("@");
            }
        }

        private void serialPort1_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {            
            try
            {
                SerialPort sp = (SerialPort)sender;
                Thread.Sleep(50);
                string indata = sp.ReadExisting();
                indata = indata.Replace('.', ',');
                var trama = indata.Split(':');
                if (trama.Length >= 3)
                {
                    chart1.Series[0].Points.AddY(((double.Parse(trama[1]) * 5000 / 1024) - 2500) / 1.3 * 0.1);
                    chart1.Series[1].Points.AddY(((double.Parse(trama[2]) * 5000 / 1024) - 2500) / 1.4 * 0.1);
                    textBox1.Text = "" + ((double.Parse(trama[1]) * 5000 / 1024) - 2500) / 1.3 * 0.1;
                    textBox2.Text = "" + ((double.Parse(trama[2]) * 5000 / 1024) - 2500) / 1.4 * 0.1;
                }
                if (chart1.Series[1].Points.Count > 50)
                {
                    chart1.Series[0].Points.RemoveAt(0);
                    chart1.Series[1].Points.RemoveAt(0);
                }
            }
            catch (Exception ex)
            {

            }
        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            chart1.Series[0].Points.Clear();
            chart1.Series[1].Points.Clear();
        }
    }
}
