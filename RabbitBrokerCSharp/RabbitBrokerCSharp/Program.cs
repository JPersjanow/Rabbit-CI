using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class SynchronousSocketClient
{

    static void Connect(String server, String message)
    {
        Int32 port = 5005;
        TcpClient client = new TcpClient(server, port);

        Byte[] data = System.Text.Encoding.ASCII.GetBytes(message);

        // Get a client stream for reading and writing.

        NetworkStream stream = client.GetStream();
        // Send the message to the connected TcpServer.
        stream.Write(data, 0, data.Length);

        Console.WriteLine("Sent: {0}", message);

        data = new Byte[256];

        while (true)
        {
            try
            {

                // String to store the response ASCII representation.
                String responseData = String.Empty;

                // Read the first batch of the TcpServer response bytes.
                Int32 bytes = stream.Read(data, 0, data.Length);
                responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                if(responseData.Length > 0 )
                {
                    Console.WriteLine("Received: {0}", responseData);
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

        

        Console.WriteLine("\n Press Enter to continue...");
        Console.Read();
    }

    public static int Main(String[] args)
    {
        Connect("127.0.0.1", "dupa");
        return 0;
    }
}