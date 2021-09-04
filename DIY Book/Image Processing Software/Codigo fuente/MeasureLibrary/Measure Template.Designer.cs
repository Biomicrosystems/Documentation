namespace MeasureLibrary
{
    partial class Measure_Template
    {
        /// <summary> 
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pbxMeasureImage = new System.Windows.Forms.PictureBox();
            this.cbxScale = new System.Windows.Forms.ComboBox();
            this.btn_Measure = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.nStartY = new System.Windows.Forms.NumericUpDown();
            this.nStartX = new System.Windows.Forms.NumericUpDown();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.nEndY = new System.Windows.Forms.NumericUpDown();
            this.nEndX = new System.Windows.Forms.NumericUpDown();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.txtAngle = new System.Windows.Forms.TextBox();
            this.txtMagnitude = new System.Windows.Forms.TextBox();
            this.txtVertical = new System.Windows.Forms.TextBox();
            this.txtHorizontal = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.nScale = new System.Windows.Forms.NumericUpDown();
            this.checkBox1 = new System.Windows.Forms.CheckBox();
            ((System.ComponentModel.ISupportInitialize)(this.pbxMeasureImage)).BeginInit();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nStartY)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.nStartX)).BeginInit();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nEndY)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.nEndX)).BeginInit();
            this.groupBox3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nScale)).BeginInit();
            this.SuspendLayout();
            // 
            // pbxMeasureImage
            // 
            this.pbxMeasureImage.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pbxMeasureImage.Location = new System.Drawing.Point(4, 4);
            this.pbxMeasureImage.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.pbxMeasureImage.Name = "pbxMeasureImage";
            this.pbxMeasureImage.Size = new System.Drawing.Size(447, 330);
            this.pbxMeasureImage.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbxMeasureImage.TabIndex = 0;
            this.pbxMeasureImage.TabStop = false;
            this.pbxMeasureImage.DragDrop += new System.Windows.Forms.DragEventHandler(this.pbxMeasureImage_DragDrop);
            this.pbxMeasureImage.DragEnter += new System.Windows.Forms.DragEventHandler(this.pbxMeasureImage_DragEnter);
            this.pbxMeasureImage.MouseClick += new System.Windows.Forms.MouseEventHandler(this.pbxMeasureImage_MouseClick);
            // 
            // cbxScale
            // 
            this.cbxScale.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbxScale.FormattingEnabled = true;
            this.cbxScale.Items.AddRange(new object[] {
            "mm",
            "um",
            "nm"});
            this.cbxScale.Location = new System.Drawing.Point(228, 344);
            this.cbxScale.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.cbxScale.Name = "cbxScale";
            this.cbxScale.Size = new System.Drawing.Size(87, 24);
            this.cbxScale.TabIndex = 2;
            // 
            // btn_Measure
            // 
            this.btn_Measure.Location = new System.Drawing.Point(4, 342);
            this.btn_Measure.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.btn_Measure.Name = "btn_Measure";
            this.btn_Measure.Size = new System.Drawing.Size(437, 28);
            this.btn_Measure.TabIndex = 3;
            this.btn_Measure.Text = "Measure";
            this.btn_Measure.UseVisualStyleBackColor = true;
            this.btn_Measure.Click += new System.EventHandler(this.btn_Measure_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.nStartY);
            this.groupBox1.Controls.Add(this.nStartX);
            this.groupBox1.Controls.Add(this.label3);
            this.groupBox1.Controls.Add(this.label2);
            this.groupBox1.Location = new System.Drawing.Point(4, 378);
            this.groupBox1.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Padding = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.groupBox1.Size = new System.Drawing.Size(215, 90);
            this.groupBox1.TabIndex = 5;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Start Point";
            // 
            // nStartY
            // 
            this.nStartY.Location = new System.Drawing.Point(43, 55);
            this.nStartY.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.nStartY.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.nStartY.Name = "nStartY";
            this.nStartY.Size = new System.Drawing.Size(164, 22);
            this.nStartY.TabIndex = 7;
            // 
            // nStartX
            // 
            this.nStartX.Location = new System.Drawing.Point(43, 23);
            this.nStartX.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.nStartX.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.nStartX.Name = "nStartX";
            this.nStartX.Size = new System.Drawing.Size(164, 22);
            this.nStartX.TabIndex = 6;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(8, 58);
            this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(25, 17);
            this.label3.TabIndex = 1;
            this.label3.Text = "Y: ";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(8, 26);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(25, 17);
            this.label2.TabIndex = 0;
            this.label2.Text = "X: ";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.nEndY);
            this.groupBox2.Controls.Add(this.nEndX);
            this.groupBox2.Controls.Add(this.label4);
            this.groupBox2.Controls.Add(this.label5);
            this.groupBox2.Location = new System.Drawing.Point(227, 378);
            this.groupBox2.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Padding = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.groupBox2.Size = new System.Drawing.Size(215, 90);
            this.groupBox2.TabIndex = 8;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "End Point";
            // 
            // nEndY
            // 
            this.nEndY.Location = new System.Drawing.Point(43, 55);
            this.nEndY.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.nEndY.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.nEndY.Name = "nEndY";
            this.nEndY.Size = new System.Drawing.Size(164, 22);
            this.nEndY.TabIndex = 7;
            // 
            // nEndX
            // 
            this.nEndX.Location = new System.Drawing.Point(43, 23);
            this.nEndX.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.nEndX.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.nEndX.Name = "nEndX";
            this.nEndX.Size = new System.Drawing.Size(164, 22);
            this.nEndX.TabIndex = 6;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(8, 58);
            this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(25, 17);
            this.label4.TabIndex = 1;
            this.label4.Text = "Y: ";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(8, 26);
            this.label5.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(25, 17);
            this.label5.TabIndex = 0;
            this.label5.Text = "X: ";
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.txtAngle);
            this.groupBox3.Controls.Add(this.txtMagnitude);
            this.groupBox3.Controls.Add(this.txtVertical);
            this.groupBox3.Controls.Add(this.txtHorizontal);
            this.groupBox3.Controls.Add(this.label9);
            this.groupBox3.Controls.Add(this.label8);
            this.groupBox3.Controls.Add(this.label6);
            this.groupBox3.Controls.Add(this.label7);
            this.groupBox3.Location = new System.Drawing.Point(4, 475);
            this.groupBox3.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Padding = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.groupBox3.Size = new System.Drawing.Size(437, 90);
            this.groupBox3.TabIndex = 9;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Measured";
            // 
            // txtAngle
            // 
            this.txtAngle.Enabled = false;
            this.txtAngle.Location = new System.Drawing.Point(300, 54);
            this.txtAngle.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtAngle.Name = "txtAngle";
            this.txtAngle.Size = new System.Drawing.Size(105, 22);
            this.txtAngle.TabIndex = 7;
            this.txtAngle.Visible = false;
            // 
            // txtMagnitude
            // 
            this.txtMagnitude.Enabled = false;
            this.txtMagnitude.Location = new System.Drawing.Point(300, 22);
            this.txtMagnitude.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtMagnitude.Name = "txtMagnitude";
            this.txtMagnitude.Size = new System.Drawing.Size(105, 22);
            this.txtMagnitude.TabIndex = 6;
            // 
            // txtVertical
            // 
            this.txtVertical.Enabled = false;
            this.txtVertical.Location = new System.Drawing.Point(96, 54);
            this.txtVertical.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtVertical.Name = "txtVertical";
            this.txtVertical.Size = new System.Drawing.Size(105, 22);
            this.txtVertical.TabIndex = 5;
            // 
            // txtHorizontal
            // 
            this.txtHorizontal.Enabled = false;
            this.txtHorizontal.Location = new System.Drawing.Point(96, 22);
            this.txtHorizontal.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtHorizontal.Name = "txtHorizontal";
            this.txtHorizontal.Size = new System.Drawing.Size(105, 22);
            this.txtHorizontal.TabIndex = 4;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(219, 26);
            this.label9.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(82, 17);
            this.label9.TabIndex = 3;
            this.label9.Text = "Magnitude: ";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(219, 58);
            this.label8.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(52, 17);
            this.label8.TabIndex = 2;
            this.label8.Text = "Angle: ";
            this.label8.Visible = false;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(8, 58);
            this.label6.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(63, 17);
            this.label6.TabIndex = 1;
            this.label6.Text = "Vertical: ";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(8, 26);
            this.label7.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(80, 17);
            this.label7.TabIndex = 0;
            this.label7.Text = "Horizontal: ";
            // 
            // nScale
            // 
            this.nScale.Location = new System.Drawing.Point(84, 346);
            this.nScale.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.nScale.Maximum = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            this.nScale.Name = "nScale";
            this.nScale.Size = new System.Drawing.Size(123, 22);
            this.nScale.TabIndex = 10;
            // 
            // checkBox1
            // 
            this.checkBox1.AutoSize = true;
            this.checkBox1.Location = new System.Drawing.Point(5, 347);
            this.checkBox1.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.checkBox1.Name = "checkBox1";
            this.checkBox1.Size = new System.Drawing.Size(65, 21);
            this.checkBox1.TabIndex = 11;
            this.checkBox1.Text = "Scale";
            this.checkBox1.UseVisualStyleBackColor = true;
            this.checkBox1.CheckedChanged += new System.EventHandler(this.checkBox1_CheckedChanged);
            // 
            // Measure_Template
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ControlLight;
            this.Controls.Add(this.btn_Measure);
            this.Controls.Add(this.checkBox1);
            this.Controls.Add(this.nScale);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.cbxScale);
            this.Controls.Add(this.pbxMeasureImage);
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Name = "Measure_Template";
            this.Size = new System.Drawing.Size(456, 575);
            this.Load += new System.EventHandler(this.Measure_Template_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pbxMeasureImage)).EndInit();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nStartY)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.nStartX)).EndInit();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nEndY)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.nEndX)).EndInit();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nScale)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pbxMeasureImage;
        private System.Windows.Forms.ComboBox cbxScale;
        private System.Windows.Forms.Button btn_Measure;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.NumericUpDown nStartY;
        private System.Windows.Forms.NumericUpDown nStartX;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.NumericUpDown nEndY;
        private System.Windows.Forms.NumericUpDown nEndX;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.TextBox txtAngle;
        private System.Windows.Forms.TextBox txtMagnitude;
        private System.Windows.Forms.TextBox txtVertical;
        private System.Windows.Forms.TextBox txtHorizontal;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.NumericUpDown nScale;
        private System.Windows.Forms.CheckBox checkBox1;
    }
}
