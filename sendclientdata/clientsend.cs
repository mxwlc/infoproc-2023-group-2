

class Program
    {
        static void Main(string[] args)
        {
            TcpListener server = new TcpListener(IPAddress, 9999);  
           // we set our IP address as server's address, and we also set the port: 9999

            server.Start();  // this will start the server

            while (true)   //we wait for a connection
            {
                TcpClient client = server.AcceptTcpClient();  //if a connection exists, the server will accept it

                NetworkStream ns = client.GetStream(); //networkstream is used to send/receive messages

                ns.Write(hello, 0, hello.Length);     //sending the message

                //SEND DATA
                string clientMessage = "this will be a string of all the variables we want to send to the server";
                byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(clientMessage);
                stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length); 





                //RECEIVE DATA
                while (client.Connected)  //while the client is connected, we look for incoming messages
                {
                    byte[] msg = new byte[1024];     //the messages arrive as byte array
                    ns.Read(msg, 0, msg.Length);   //the same networkstream reads the message sent by the client
                    Console.WriteLine(encoder.GetString(msg).Trim('')); //now , we write the message as string
                }
            }

        }
    }

using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;      
using System.Net.Sockets;  
using System.Threading;


class Program
    {

        static void Main(string[] args)
        {
            Program main = new Program();
            main.server_start();  //starting the server

            Console.ReadLine();  
        }

        TcpListener server = new TcpListener(IPAddress.Any, 9999);   

        private void server_start()
        {
            server.Start();    
            accept_connection();  //accepts incoming connections
        }

        private void accept_connection()
        {
            server.BeginAcceptTcpClient(handle_connection, server);  //this is called asynchronously and will run in a different thread
        }

        private void handle_connection(IAsyncResult result)  //the parameter is a delegate, used to communicate between threads
        {
            accept_connection();  //once again, checking for any other incoming connections
            TcpClient client = server.EndAcceptTcpClient(result);  //creates the TcpClient

            NetworkStream ns = client.GetStream();

            

        }

    }
}

 

 



