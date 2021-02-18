using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class SynchronousSocketClient
{
    Int32 port = 0;
    String server = null;

    public void RabbitInfoUser()
    {
        Console.WriteLine("Enter Rabbit server ip:");
        server = Console.ReadLine();
        Console.WriteLine("Enter port to connect, if empty will default to 5005");
        String port_user = Console.ReadLine();
        if (port_user == "")
        {
            Console.WriteLine("Default port set to {0}", port);
        }
        else
        {
            port = System.Convert.ToInt32(port_user);
        }
    }
    public void Connect(String message)
    {
        Int32 port = 5005;
        TcpClient client = null;
        Int32 bytes = 0;
        while (client == null)
        {
            try
            {
                client = new TcpClient(server, port);

            }
            catch (SocketException e)
            {
                Console.WriteLine(e);
                Console.WriteLine("To retry -r, to exit -e");
                String some_command = Console.ReadLine();

                if (some_command == "e")
                {
                    Environment.Exit(1);
                }
            }
        }

        Byte[] data = System.Text.Encoding.ASCII.GetBytes(message);

        // Get a client stream for reading and writing.

        NetworkStream stream = client.GetStream();
        // Send the message to the connected TcpServer.
        //stream.Write(data, 0, data.Length);

        //Console.WriteLine("Sent: {0}", message);

        data = new Byte[1024];

        while (true)
        {
            try
            {

                // String to store the response ASCII representation.
                String responseData = String.Empty;

                // Read the first batch of the TcpServer response bytes.
                bytes = stream.Read(data, 0, data.Length);
                responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                if(responseData.Length > 0 )
                {
                    Console.WriteLine("Received: {0}", responseData);
                    if (responseData.Equals("/K ping wp.pl"))
                    {
                        System.Diagnostics.Process.Start("CMD.exe", responseData);
                    }
                }

            }
            catch (ArgumentNullException e)
            {
                Console.WriteLine("ArgumentNullException: {0}", e);
                // Close everything.
                stream.Close();
                client.Close();
            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
                // Close everything.
                stream.Close();
                client.Close();
            }
        }
    }

    public void RunCommand(String command)
    {
        System.Diagnostics.Process.Start("CMD.exe", command);
    }

    public static int Main(String[] args)
    {
        SynchronousSocketClient SocketClient = new SynchronousSocketClient();
        SocketClient.RabbitInfoUser();
        SocketClient.Connect("message");
        return 0;
    }
}