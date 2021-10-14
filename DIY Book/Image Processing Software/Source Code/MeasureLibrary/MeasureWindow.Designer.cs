namespace MeasureLibrary
{
    partial class MeasureWindow
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
            this.components = new System.ComponentModel.Container();
            this.pbxBigImage = new System.Windows.Forms.PictureBox();
            this.pbxZoomImage = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            this.txtDist = new System.Windows.Forms.TextBox();
            this.txt_pixels = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.txt_final = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.btn_measure = new System.Windows.Forms.Button();
            this.comboBox1 = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.txtScale = new System.Windows.Forms.TextBox();
            this.comboBox2 = new System.Windows.Forms.ComboBox();
            this.btn_save = new System.Windows.Forms.Button();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.size100x100ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.size200x200ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.size300x300ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.size400x400ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            ((System.ComponentModel.ISupportInitialize)(this.pbxBigImage)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxZoomImage)).BeginInit();
            this.contextMenuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // pbxBigImage
            // 
            this.pbxBigImage.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pbxBigImage.ContextMenuStrip = this.contextMenuStrip1;
            this.pbxBigImage.Location = new System.Drawing.Point(4, 4);
            this.pbxBigImage.Margin = new System.Windows.Forms.Padding(4);
            this.pbxBigImage.Name = "pbxBigImage";
            this.pbxBigImage.Size = new System.Drawing.Size(400, 400);
            this.pbxBigImage.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbxBigImage.TabIndex = 0;
            this.pbxBigImage.TabStop = false;
            this.pbxBigImage.DragDrop += new System.Windows.Forms.DragEventHandler(this.pbxBigImage_DragDrop);
            this.pbxBigImage.DragEnter += new System.Windows.Forms.DragEventHandler(this.pbxBigImage_DragEnter);
            this.pbxBigImage.MouseDown += new System.Windows.Forms.MouseEventHandler(this.pbxBigImage_MouseDown);
            this.pbxBigImage.MouseMove += new System.Windows.Forms.MouseEventHandler(this.pbxBigImage_MouseMove);
            this.pbxBigImage.MouseUp += new System.Windows.Forms.MouseEventHandler(this.pbxBigImage_MouseUp);
            // 
            // pbxZoomImage
            // 
            this.pbxZoomImage.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pbxZoomImage.Location = new System.Drawing.Point(429, 4);
            this.pbxZoomImage.Margin = new System.Windows.Forms.Padding(4);
            this.pbxZoomImage.Name = "pbxZoomImage";
            this.pbxZoomImage.Size = new System.Drawing.Size(200, 200);
            this.pbxZoomImage.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pbxZoomImage.TabIndex = 1;
            this.pbxZoomImage.TabStop = false;
            this.pbxZoomImage.MouseClick += new System.Windows.Forms.MouseEventHandler(this.pbxZoomImage_MouseClick);
            this.pbxZoomImage.MouseEnter += new System.EventHandler(this.pbxZoomImage_MouseEnter);
            this.pbxZoomImage.MouseLeave += new System.EventHandler(this.pbxZoomImage_MouseLeave);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(410, 269);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(63, 17);
            this.label1.TabIndex = 2;
            this.label1.Text = "Distance";
            // 
            // txtDist
            // 
            this.txtDist.Location = new System.Drawing.Point(479, 266);
            this.txtDist.Name = "txtDist";
            this.txtDist.Size = new System.Drawing.Size(92, 22);
            this.txtDist.TabIndex = 2;
            // 
            // txt_pixels
            // 
            this.txt_pixels.Location = new System.Drawing.Point(461, 294);
            this.txt_pixels.Name = "txt_pixels";
            this.txt_pixels.Size = new System.Drawing.Size(110, 22);
            this.txt_pixels.TabIndex = 4;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(411, 297);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(44, 17);
            this.label2.TabIndex = 4;
            this.label2.Text = "Pixels";
            // 
            // txt_final
            // 
            this.txt_final.Location = new System.Drawing.Point(479, 351);
            this.txt_final.Name = "txt_final";
            this.txt_final.Size = new System.Drawing.Size(92, 22);
            this.txt_final.TabIndex = 6;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(410, 354);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(63, 17);
            this.label3.TabIndex = 6;
            this.label3.Text = "Distance";
            // 
            // btn_measure
            // 
            this.btn_measure.Location = new System.Drawing.Point(413, 322);
            this.btn_measure.Name = "btn_measure";
            this.btn_measure.Size = new System.Drawing.Size(232, 23);
            this.btn_measure.TabIndex = 5;
            this.btn_measure.Text = "Measure";
            this.btn_measure.UseVisualStyleBackColor = true;
            this.btn_measure.Click += new System.EventHandler(this.btn_measure_Click);
            // 
            // comboBox1
            // 
            this.comboBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox1.FormattingEnabled = true;
            this.comboBox1.Items.AddRange(new object[] {
            "mm",
            "um",
            "nm"});
            this.comboBox1.Location = new System.Drawing.Point(578, 238);
            this.comboBox1.Name = "comboBox1";
            this.comboBox1.Size = new System.Drawing.Size(67, 24);
            this.comboBox1.TabIndex = 1;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(410, 241);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(43, 17);
            this.label4.TabIndex = 10;
            this.label4.Text = "Scale";
            // 
            // txtScale
            // 
            this.txtScale.Location = new System.Drawing.Point(459, 238);
            this.txtScale.Name = "txtScale";
            this.txtScale.Size = new System.Drawing.Size(112, 22);
            this.txtScale.TabIndex = 0;
            // 
            // comboBox2
            // 
            this.comboBox2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox2.FormattingEnabled = true;
            this.comboBox2.Items.AddRange(new object[] {
            "mm",
            "um",
            "nm"});
            this.comboBox2.Location = new System.Drawing.Point(577, 266);
            this.comboBox2.Name = "comboBox2";
            this.comboBox2.Size = new System.Drawing.Size(67, 24);
            this.comboBox2.TabIndex = 3;
            // 
            // btn_save
            // 
            this.btn_save.Location = new System.Drawing.Point(414, 381);
            this.btn_save.Name = "btn_save";
            this.btn_save.Size = new System.Drawing.Size(230, 23);
            this.btn_save.TabIndex = 7;
            this.btn_save.Text = "Save as ...";
            this.btn_save.UseVisualStyleBackColor = true;
            this.btn_save.Click += new System.EventHandler(this.btn_save_Click);
            // 
            // saveFileDialog1
            // 
            this.saveFileDialog1.Filter = "Jpg File|*.jpg";
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.contextMenuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.size100x100ToolStripMenuItem,
            this.size200x200ToolStripMenuItem,
            this.size300x300ToolStripMenuItem,
            this.size400x400ToolStripMenuItem});
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(124, 108);
            // 
            // size100x100ToolStripMenuItem
            // 
            this.size100x100ToolStripMenuItem.Name = "size100x100ToolStripMenuItem";
            this.size100x100ToolStripMenuItem.Size = new System.Drawing.Size(181, 26);
            this.size100x100ToolStripMenuItem.Text = "Size 1";
            this.size100x100ToolStripMenuItem.Click += new System.EventHandler(this.size100x100ToolStripMenuItem_Click);
            // 
            // size200x200ToolStripMenuItem
            // 
            this.size200x200ToolStripMenuItem.Name = "size200x200ToolStripMenuItem";
            this.size200x200ToolStripMenuItem.Size = new System.Drawing.Size(181, 26);
            this.size200x200ToolStripMenuItem.Text = "Size 2";
            this.size200x200ToolStripMenuItem.Click += new System.EventHandler(this.size200x200ToolStripMenuItem_Click);
            // 
            // size300x300ToolStripMenuItem
            // 
            this.size300x300ToolStripMenuItem.Name = "size300x300ToolStripMenuItem";
            this.size300x300ToolStripMenuItem.Size = new System.Drawing.Size(181, 26);
            this.size300x300ToolStripMenuItem.Text = "Size 3";
            this.size300x300ToolStripMenuItem.Click += new System.EventHandler(this.size300x300ToolStripMenuItem_Click);
            // 
            // size400x400ToolStripMenuItem
            // 
            this.size400x400ToolStripMenuItem.Name = "size400x400ToolStripMenuItem";
            this.size400x400ToolStripMenuItem.Size = new System.Drawing.Size(181, 26);
            this.size400x400ToolStripMenuItem.Text = "Size 4";
            this.size400x400ToolStripMenuItem.Click += new System.EventHandler(this.size400x400ToolStripMenuItem_Click);
            // 
            // MeasureWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.btn_save);
            this.Controls.Add(this.comboBox2);
            this.Controls.Add(this.txtScale);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.comboBox1);
            this.Controls.Add(this.btn_measure);
            this.Controls.Add(this.txt_final);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.txt_pixels);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.txtDist);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.pbxZoomImage);
            this.Controls.Add(this.pbxBigImage);
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "MeasureWindow";
            this.Size = new System.Drawing.Size(650, 410);
            this.Load += new System.EventHandler(this.MeasureWindow_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pbxBigImage)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pbxZoomImage)).EndInit();
            this.contextMenuStrip1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pbxBigImage;
        private System.Windows.Forms.PictureBox pbxZoomImage;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtDist;
        private System.Windows.Forms.TextBox txt_pixels;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox txt_final;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button btn_measure;
        private System.Windows.Forms.ComboBox comboBox1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox txtScale;
        private System.Windows.Forms.ComboBox comboBox2;
        private System.Windows.Forms.Button btn_save;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.ToolStripMenuItem size100x100ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem size200x200ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem size300x300ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem size400x400ToolStripMenuItem;
    }
}
