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
    public partial class Form2 : Form
    {
        string HOST = "127.0.0.1";
        string PORT = "40000";
        public Form2()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void Wait()
        {
            for (int i = 0; i <= 1000000; i++)
                continue;
        }

        private void button2_Click(object sender, EventArgs e)
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

            string username = textBox1.Text;
            string password = textBox2.Text;
            string name = textBox3.Text;
            if (username.Length == 0)
                username = "1";
            if (password.Length == 0)
                password = "1";
            if (name.Length == 0)
                name = "1";
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
            string code = "00000005";
            Byte[] code_data = System.Text.Encoding.ASCII.GetBytes(code);
            Byte[] username_data = System.Text.Encoding.ASCII.GetBytes(username);
            Byte[] password_data = System.Text.Encoding.ASCII.GetBytes(password);
            Byte[] name_data = System.Text.Encoding.ASCII.GetBytes(name);
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
                stream.Write(username_data, 0, username_data.Length);
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
            stream.Read(code_data, 0, 8);
            code = System.Text.Encoding.ASCII.GetString(code_data);
            if (code == "00000006")
                MessageBox.Show( "Sign in successful!", "Information", MessageBoxButtons.OK);
            else if (code == "00000007")
                MessageBox.Show( "Username already used!", "Warning", MessageBoxButtons.OK);
            else if (code == "00000008")
                MessageBox.Show( "Please complete all fields!", "Warning", MessageBoxButtons.OK);
            else if (code == "00000009")
                MessageBox.Show( "Can not connect to server", "Warning", MessageBoxButtons.OK);
        }

    private void button3_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }
    }
}
