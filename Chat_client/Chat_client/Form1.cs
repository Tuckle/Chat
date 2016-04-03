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
        string PORT = "50000";
        public Form1()
        {
            InitializeComponent();
            
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
            client.Connect(ep);
            string name = textBox1.Text;
            string password = textBox2.Text;
            NetworkStream stream = client.GetStream();
            Byte[] name_data = System.Text.Encoding.ASCII.GetBytes(name);
            Byte[] password_data = System.Text.Encoding.ASCII.GetBytes(password);
            string code = "00000004";
            Byte[] code_data = System.Text.Encoding.ASCII.GetBytes(code);
            stream.Write(code_data, 0, code_data.Length);
            int i = 0;
            while (i < 1000000)
                i++;
            stream.Write(name_data, 0, name_data.Length);
            i = 0;
            while (i < 1000000)
                i++;
            stream.Write(password_data, 0, password_data.Length);
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
    }
}