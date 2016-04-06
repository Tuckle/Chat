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
    public partial class Form3 : Form
    {
        TcpClient client;
        NetworkStream stream;
        IPEndPoint ep;
        public Form3()
        {
            InitializeComponent();
        }

        public Form3(TcpClient client1,NetworkStream stream1, IPEndPoint ep1)
        {
            InitializeComponent();
            this.client = client1;
            this.stream = stream1;
            this.ep = ep1;
        }
        
        private void Wait()
        {
            for (int i = 0; i <= 1000000; i++)
                continue;
        }

        private void SignOut()
        {
            string msg = "00000010";
            Byte[] msg_data = System.Text.Encoding.ASCII.GetBytes(msg);
            stream.Write(msg_data, 0, msg_data.Length);
            Wait();
            stream.Close();
            client.Close();
        }

        private void systemToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SignOut();
            Application.Exit();
        }

        private void signOutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SignOut();
            this.Close();
        }
        ~Form3()
        {
            SignOut();
        }
    }
}
