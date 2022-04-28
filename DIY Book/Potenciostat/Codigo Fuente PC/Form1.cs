using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Quobject.SocketIoClientDotNet.Client;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;

namespace Potentiostat_web
{
    enum CMD
    {
        cmd_stop = 1 << 0,
        cmd_start = 1 << 1,
        cmd_set_low = 1 << 2,
        cmd_set_high = 1 << 3,
        cmd_set_speed = 1 << 4,
        cmd_test_write = 1 << 5,
        cmd_test_read = 1 << 6,
        cmd_version = 1 << 7
    };
    public partial class Form1 : Form
    {
        private double zero_correction = 0.0;
        public Form1()
        {
            InitializeComponent();
            serialPort1.DataReceived += SerialPort1_DataReceived;
            chart1.ChartAreas.FirstOrDefault().AxisX.LabelStyle.Format = "#.###";
            chart2.ChartAreas.FirstOrDefault().AxisX.LabelStyle.Format = "#.###";
            JObject configurations = JObject.Parse(File.ReadAllText(@"appConfig.json"));
            zero_correction = Convert.ToDouble(configurations["zero_correction"]);
            tbx_server_url.Text = Convert.ToString(configurations["RemoteServer"]);
        }

        #region Potentiostat
        #region Variables
        int version = 1;
        int[] data_rcv = new int[4];
        double dato1, dato2;
        double resoulution = 4096.0;
        Stopwatch clock;
        bool d = true;

        byte[] buff = new byte[5];
        enum Commands
        {
            StartID = 0xA0,
            EndPKG = 0xAB,
            StartMeasurement = 0x01,
            StoptMeasurement = 0x02,
            SetStartPoint = 0x03,
            SetZeroCross = 0x04,
            SetFirstVertex = 0x05,
            SetSecondVeretex = 0x06,
            setSpeed = 0x07,
            SetTimeHold = 0x11,
            SetFinalValue = 0x12,
            ACK = 0xB0,
            ENDRUN = 0xB1
        }
        #endregion
        #region Methods
        private void refreshPorts()
        {
            string[] portNames = SerialPort.GetPortNames();
            cbxPorts.Items.Clear();
            foreach (string port in portNames)
            {
                cbxPorts.Items.Add(port);
                cbxPorts.SelectedIndex = 0;
            }
        }

        private void SerialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            try
            {
                if (serialPort1.IsOpen)
                {
                    while (serialPort1.BytesToRead > 0)
                    {
                        if (d)
                            clock = Stopwatch.StartNew();
                        else
                        {
                            clock.Stop();
                            if (txtData.InvokeRequired)
                            {
                                txtData.Invoke(new MethodInvoker(delegate
                                {
                                    txtData.Text = "t: " + clock.ElapsedMilliseconds + "\r\n";
                                }));

                            }
                        }
                        byte c = (byte)serialPort1.ReadByte();
                        switch ((Commands)c)
                        {
                            case Commands.StartID:
                                data_rcv[0] = serialPort1.ReadChar();
                                data_rcv[1] = serialPort1.ReadChar();
                                data_rcv[2] = serialPort1.ReadChar();
                                data_rcv[3] = serialPort1.ReadChar();
                                dato1 = ((data_rcv[0] << 6) & 0x0FC0) | data_rcv[1];
                                dato2 = ((data_rcv[2] << 6) & 0x0FC0) | data_rcv[3];

                                switch (version)
                                {
                                    case 1: // Primera version del potenciostato
                                        dato1 = (double)((dato1 - (resoulution / 2)) * (3.3 / resoulution));
                                        dato2 = (double)((dato2 - (resoulution / 2)) * (3.3 / resoulution));
                                        break;
                                    case 2: // Segunda version del potenciostato
                                        if (dato1 > 2048)
                                            dato1 = (((Int16)dato1) | 0xF000);
                                        dato1 = -(double)((Int16)dato1 * 0.001);
                                        if (dato2 > 2048)
                                            dato2 = (((Int16)dato2) | 0xF000);
                                        dato2 = -(double)((Int16)dato2 * 0.001);

                                        break;
                                    default:
                                        dato1 = (double)((dato1 - (resoulution / 2)) * (3.3 / resoulution));
                                        dato2 = (double)((dato2 - (resoulution / 2)) * (3.3 / resoulution));
                                        break;
                                }

                                //Invert current
                                dato2 = dato2 + zero_correction; // Zero correction

                                var dataADC = new { dat1 = dato1, dat2 = dato2 };
                                if (socket != null)
                                    socket.Emit("ADC_values", JsonConvert.SerializeObject(dataADC));

                                if (chart1.InvokeRequired)
                                {
                                    chart1.Invoke(new MethodInvoker(delegate
                                    {
                                        chart1.Series[0].Points.AddY(dato1);
                                        chart1.Series[1].Points.AddY(dato2);
                                    }));
                                }
                                if (chart2.InvokeRequired)
                                {
                                    chart2.Invoke(new MethodInvoker(delegate
                                    {
                                        chart2.Series[0].Points.AddXY(dato1, dato2);
                                    }));
                                }
                                serialPort1.ReadExisting();
                                d = !d;
                                break;
                            case Commands.ACK:
                                byte msg = (byte)serialPort1.ReadByte();
                                if (msg == (byte)Commands.ENDRUN)
                                {
                                    if (btnStart.InvokeRequired)
                                    {
                                        btnStart.Invoke(new MethodInvoker(delegate
                                        {
                                            btnStart.Enabled = true;
                                            btnSndSpeed.Enabled = true;
                                            btnSndSP.Enabled = true;
                                            btnSndFV.Enabled = true;
                                            btnSndSV.Enabled = true;
                                            btnSndZC.Enabled = true;
                                            btnSendAll.Enabled = true;
                                            btnStop.Enabled = false;

                                        }));
                                    }
                                }
                                break;
                            default:
                                break;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                if (serialPort1.IsOpen)
                    serialPort1.Close();
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            refreshPorts();
            chart1.Series[0].Points.Clear();
            chart1.Series[1].Points.Clear();

            chart2.Series[0].Points.Clear();
            chart2.Series[1].Points.Clear();
        }

        private void btnRefhresh_Click(object sender, EventArgs e)
        {
            refreshPorts();
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            txtData.Clear();
            chart1.Series[0].Points.Clear();
            chart1.Series[1].Points.Clear();
            chart2.Series[0].Points.Clear();
        }

        private void btnSndSP_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                int dato = (int)(((double)numSP.Value + (3.3 / 2.0)) / 3.3 * resoulution) - 1;
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.SetStartPoint;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnSndFV_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                int dato = (int)(((double)numFV.Value + (3.3 / 2.0)) / 3.3 * resoulution) - 1;
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.SetFirstVertex;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnSndSV_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                int dato = (int)(((double)numSV.Value + (3.3 / 2.0)) / 3.3 * resoulution) - 1;
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.SetSecondVeretex;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnSndZC_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                int dato = (int)numZC.Value;
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.SetZeroCross;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnSndSpeed_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;

                int dato = (int)((double)numSpeed.Value / 0.0008);
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.setSpeed;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                buff[1] = (byte)Commands.StartMeasurement;
                buff[2] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 3);
            }
            btnStart.Enabled = false;
            btnSndSP.Enabled = false;
            btnSndFV.Enabled = false;
            btnSndSV.Enabled = false;
            btnSndZC.Enabled = false;
            btnSendAll.Enabled = false;
            btnSndSpeed.Enabled = false;

            btnStop.Enabled = true;
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                buff[1] = (byte)Commands.StoptMeasurement;
                buff[2] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 3);
            }
            btnStart.Enabled = true;
            btnSndSP.Enabled = true;
            btnSndFV.Enabled = true;
            btnSndSV.Enabled = true;
            btnSndZC.Enabled = true;
            btnSndSpeed.Enabled = true;
            btnSendAll.Enabled = true;
            btnStop.Enabled = false;
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            using (SaveFileDialog sfd = new SaveFileDialog())
            {
                sfd.Filter = "txt files (*.txt)|*.txt";
                if (sfd.ShowDialog(this) == DialogResult.OK)
                {
                    if (sfd.FileName != "")
                    {
                        using (StreamWriter sw = new StreamWriter(sfd.FileName))
                        {
                            sw.WriteLine("Log of Potentiostat Software Version 2.0");
                            sw.Write(DateTime.Now.ToLongDateString());
                            sw.Write("\t\t");
                            sw.WriteLine(DateTime.Now.ToLongTimeString());
                            sw.WriteLine("");
                            sw.WriteLine(String.Format("{0,15}={1,7} V", "Start Point", (double)numSP.Value));
                            sw.WriteLine(String.Format("{0,15}={1,7} V", "First Vertex", numFV.Value));
                            sw.WriteLine(String.Format("{0,15}={1,7} V", "Second Vertex", numSV.Value));
                            sw.WriteLine(String.Format("{0,15}={1,7} ", "Zero cross", numZC.Value));
                            sw.WriteLine(String.Format("{0,15}={1,7} ", "Speed", numSpeed.Value));
                            sw.WriteLine("");
                            sw.WriteLine(String.Format("{0,10}\t|{1,20}\t|{2,20}", "Position", "Voltaje", "Current"));
                            for (int i = 0; i < chart1.Series[0].Points.Count; i++)
                            {
                                sw.WriteLine(String.Format("{0,10}\t;{1,20}\t;{2,20}", i,
                                    chart1.Series[0].Points[i].YValues[0],
                                    chart1.Series[1].Points[i].YValues[0]));
                            }
                            chart1.Width = 1024;
                            chart1.Height = 768;
                            chart2.Width = 1024;
                            chart2.Height = 768;
                            chart1.SaveImage(sfd.FileName.Remove(sfd.FileName.Length - 4, 4) + "_A.png", ChartImageFormat.Png);
                            chart2.SaveImage(sfd.FileName.Remove(sfd.FileName.Length - 4, 4) + "_B.png", ChartImageFormat.Png);
                            sw.Close();
                        }
                    }
                }
            }
        }

        private void btnSendAll_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)0xC0;
                serialPort1.Write(buff, 0, 1);
            }
            btnSndSP_Click(null, null);
            btnSndFV_Click(null, null);
            btnSndSV_Click(null, null);
            btnSndZC_Click(null, null);
            btnSndSpeed_Click(null, null);
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (serialPort1.IsOpen)
                serialPort1.Close();
        }

        private void btnASVSendAll_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)0xC1;
                serialPort1.Write(buff, 0, 1);
            }
            btnASSP_Click(null, null);
            btnASFV_Click(null, null);
            btnASTH_Click(null, null);
            btnASSR_Click(null, null);
        }

        private void btnASSP_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                int dato = (int)(((double)numASSP.Value + (3.3 / 2.0)) / 3.3 * resoulution) - 1;
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.SetStartPoint;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnASFV_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                int dato = (int)(((double)numASFV.Value + (3.3 / 2.0)) / 3.3 * resoulution) - 1;
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.SetFinalValue;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnASTH_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;
                int dato = (int)((double)numASTH.Value * 10);
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.SetTimeHold;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnASSR_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)Commands.StartID;

                int dato = (int)((double)numASSR.Value / 0.0008);
                byte[] bytes = BitConverter.GetBytes(dato);
                buff[1] = (byte)Commands.setSpeed;
                buff[2] = (byte)(bytes[0] & 0x3F);
                buff[3] = (byte)(((bytes[1] << 2) & 0xFC) | ((bytes[0] >> 6) & 0x03));
                buff[4] = (byte)Commands.EndPKG;
                serialPort1.Write(buff, 0, 5);
            }
        }

        private void btnSWASVSend_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                buff[0] = (byte)0xC2;
                serialPort1.Write(buff, 0, 1);
            }
            btnASSP_Click(null, null);
            btnASFV_Click(null, null);
            btnASTH_Click(null, null);
            btnASSR_Click(null, null);
        }

        private void btnConnect_Click(object sender, EventArgs e)
        {
            if (((Button)sender).Text == "Connect")
            {
                if (serialPort1.IsOpen)
                    serialPort1.Close();
                serialPort1.PortName = (string)cbxPorts.SelectedItem;
                try
                {
                    serialPort1.Open();
                }
                catch (Exception ex)
                {
                }
                ((Button)sender).Text = "Disconnect";
            }
            else
            {
                if (serialPort1.IsOpen)
                    serialPort1.Close();
                ((Button)sender).Text = "Connect";
            }
        }

        #endregion
        #endregion

        #region Web connection
        #region Variables
        Socket socket;

        public delegate void UpdateTextMethod(string text);

        #endregion

        #region Methods
        private void btn_start_socket_Click(object sender, EventArgs e)
        {
            if (btn_start_socket.Text == "Start Socket")
            {
                socketIoManager();
                var data = new { name = "potenciostato" };
                socket.Emit("device", JsonConvert.SerializeObject(data));
                btn_start_socket.Text = "Stop Socket";
            }
            else
            {
                socket.Disconnect();
                btn_start_socket.Text = "Start Socket";
            }
        }

        private void socketIoManager()
        {
            // Conexion socket a server url
            socket = IO.Socket(tbx_server_url.Text);
            // Evento de conexión
            socket.On(Socket.EVENT_CONNECT, () =>
            {
                UpdateStatus("Socket: Connected");
            });
            // Evento de desconexión
            socket.On(Socket.EVENT_DISCONNECT, () =>
            {
                UpdateStatus("Socket: Disconnected");
            });
            // recibir data potenciostato
            socket.On("setData", (datos) =>
            {
                UpdateData(datos.ToString());
            });

            // recibir data potenciostato
            socket.On("setStart", () =>
            {
                setCommand("Start");
            });

            socket.On("setStop", () =>
            {
                setCommand("Stop");
            });


            // recibir chat
            socket.On("nuevo_mensaje", (datos) =>
            {
                var data = new { user = "", mensaje = "" };
                var datValue = JsonConvert.DeserializeAnonymousType(datos.ToString(), data);
                var t = data.GetType().ToString();
                //UpdateChat(((string)datValue.user + ": " + (string)datValue.mensaje));
            });

            socket.On("setLed", (datos) =>
            {
                //ledStatus = !ledStatus;
                //UpdateLed(ledStatus);
            });

            socket.On("startADC", (datos) =>
            {
                if (serialPort1.IsOpen)
                    serialPort1.Write("C");
            });
        }

        private void setCommand(string text)
        {
            if (btnStart.InvokeRequired)
            {
                UpdateTextMethod del = new UpdateTextMethod(setCommand);
                this.Invoke(del, new object[] { text });
            }
            else
            {
                switch (text)
                {
                    case "Start":
                        this.btnStart_Click(null, null);
                        break;
                    case "Stop":
                        this.btnStop_Click(null, null);
                        break;
                    default:
                        break;
                }
            }
        }

        private void UpdateData(string text)
        {
            if (this.numSP.InvokeRequired)
            {
                UpdateTextMethod del = new UpdateTextMethod(UpdateData);
                this.Invoke(del, new object[] { text });
            }
            else
            {
                var data = new { sp = "", fv = "", sv = "", zc = "", sr = "" };
                var datValue = JsonConvert.DeserializeAnonymousType(text.Replace('.', ','), data);

                this.numSP.Value = decimal.Parse(datValue.sp);
                this.numFV.Value = decimal.Parse(datValue.fv);
                this.numSV.Value = decimal.Parse(datValue.sv);
                this.numZC.Value = decimal.Parse(datValue.zc);
                this.numSpeed.Value = decimal.Parse(datValue.sr);

                btnSendAll_Click(null, null);
            }
        }
        private void UpdateStatus(string text)
        {
            if (this.statusStrip1.InvokeRequired)
            {
                UpdateTextMethod del = new UpdateTextMethod(UpdateStatus);
                this.Invoke(del, new object[] { text });
            }
            else
            {
                this.toolStripStatusLabel1.Text = text;
            }
        }


        #endregion

        #endregion
    }
}
