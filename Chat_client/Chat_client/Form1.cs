using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.Net;
using System.Net.Mail;

namespace Chat_client
{
    public partial class Form1 : Form
    {
        string HOST = "127.0.0.1";
        string PORT = "40000";
        public Form1()
        {
            InitializeComponent();

        }

        private void Wait()
        {
            for (int i = 0; i <= 1000000; i++)
                continue;
        }

        private void button2_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            TcpClient client = new TcpClient();
            IPEndPoint ep = new IPEndPoint(IPAddress.Parse(HOST), int.Parse(PORT));
            try
            {
                client.Connect(ep);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Can not conncet to server.", "Warning", MessageBoxButtons.OK);
                return;
            }
            
            string name = textBox1.Text;
            string password = textBox2.Text;
            if (name.Length == 0)
                name = "1";
            if (password.Length == 0)
                password = "1";
            NetworkStream stream;
            try
            {
                stream = client.GetStream();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Can not conncet to server.", "Warning", MessageBoxButtons.OK);
                return;
            }
            Byte[] name_data = System.Text.Encoding.ASCII.GetBytes(name);
            Byte[] password_data = System.Text.Encoding.ASCII.GetBytes(password);
            string code = "00000004";
            Byte[] code_data = System.Text.Encoding.ASCII.GetBytes(code);
            try
            {
                stream.Write(code_data, 0, code_data.Length);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Can not conncet to server.", "Warning", MessageBoxButtons.OK);
                return;
            }
            Wait();
            try
            {
                stream.Write(name_data, 0, name_data.Length);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Can not conncet to server.", "Warning", MessageBoxButtons.OK);
                return;
            }
            Wait();
            try
            {
                stream.Write(password_data, 0, password_data.Length);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Can not conncet to server.", "Warning", MessageBoxButtons.OK);
                return;
            }
            stream.Read(code_data, 0, 8);
            code = System.Text.Encoding.ASCII.GetString(code_data);
            if (code == "00000002")
            {
                string message = "Invaild username or password!";
                string title = "Warning";
                MessageBoxButtons b = MessageBoxButtons.OK;
                MessageBox.Show(message, title, b);
                stream.Close();
                client.Close();
            }
            else if(code =="00000001")
            {
                MessageBox.Show("Log in Successful!", "Information", MessageBoxButtons.OK);
                Form3 form = new Form3();
                form.Show();
                form.FormClosed += new FormClosedEventHandler(form_FormClose);
                this.Hide();
            }
                
        }

        private void form_FormClose(object seder,EventArgs e)
        {
            this.Show();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            Form2 form = new Form2();
            form.Show();
            form.FormClosed += new FormClosedEventHandler(form_FormClose);
            this.Hide();
            
        }

        private void form_FormClose(object sender, FormClosedEventArgs e)
        {
            this.Show();
        }
    }
}