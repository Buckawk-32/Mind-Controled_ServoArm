using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;
using UnityEngine;

public class UnityServer : MonoBehaviour
{
    class ClientData : IDisposable
    {
        // TODO: Rewrite the devID { get; private set; } --> to have saveDevID 
        public string devID { get; private set; }
        public TcpClient client { get; private set; }
        public TextReader streamReader { get; private set; }
        public TextWriter streamWriter { get; private set; }

        public ClientData(TcpClient client)
        {
            this.client = client;

            NetworkStream networkStream = client.GetStream();

            streamReader = new StreamReader(networkStream);
            streamWriter = new StreamWriter(networkStream);
        }

        public async Task SaveDevId()
        {
            Debug.LogWarning("check this shit");
            string msg;
            msg = await streamReader.ReadLineAsync();
            Debug.LogWarning("burn the book yea");

            if (msg != "" && msg != null)
            {
                if (msg.StartsWith("CON:"))
                {
                    Debug.LogWarning("NEW CILENT:" + msg.Substring(4));
                    await streamWriter.WriteLineAsync($"  {msg.Substring(4)} -- CONNECTED SUCCESFULLY  ");
                    await streamWriter.FlushAsync();

                    devID = msg.Substring(4);
                }
            }
            else
            {
                devID = "NONE";
            }
        }

        public void Dispose()
        {
            if (devID == "NONE")
            {
                Debug.LogWarning($"Closing{devID}!");
            }
            streamReader.Close();
            streamWriter.Close();
            client.Close();
        }
        
        public override string ToString()
        {
            return $"CLIENT:{devID}";
        }
    }

// ------------------------------------------------------------------------
    private static TcpListener server { get; set; }
    private static bool isServerRunning { get; set; }
    private static int portNumber = 25001;
    private static IPAddress addr = IPAddress.Parse("10.79.40.170");
    private static List<ClientData> clientList = new List<ClientData>();
    // ------------------------------------------------------------------------
    private static readonly object _lock = new object();
// ------------------------------------------------------------------------
    public static OVRHand hand;
    public static OVRSkeleton.BoneId boneId;
    public static UnityEngine.Vector3 bonePosition;
    public static UnityEngine.Quaternion boneRotation;
// ------------------------------------------------------------------------

    public static async Task StartServer()
    {
        server = new TcpListener(addr, portNumber);
        server.Start();
        print("Server Started...");
        isServerRunning = true;

        while (true)
        {
            var client = await server.AcceptTcpClientAsync();
            Debug.LogWarning("Accepted New Client...");
            var currentTask = StartConnectionAsync(client);
            if (currentTask.IsFaulted)
            {
                currentTask.Wait();
            }
        }
    }

    private async static Task StartConnectionAsync(TcpClient client)
    {
        ClientData clientData = new ClientData(client);
        Debug.LogWarning("hehe");
        lock (_lock)
        {
            clientList.Add(clientData);
        }
        Task taskDevID = Task.Run(async () => await clientData.SaveDevId());
        if (taskDevID.IsFaulted)
        {
            taskDevID.Wait();
        }

        try
        {
            if (!string.IsNullOrEmpty(clientData.devID) && clientData.devID != "NONE")
            {
                Debug.LogWarning("dodudou");
                await HandleClientAsync(clientData);
            }
        }
        catch (Exception e)
        {
            Debug.LogError(e);
        }
        finally
        {
            lock (_lock)
            {
                clientList.Remove(clientData);
            }
            clientData.Dispose();
        }
    }

    private static async Task HandleClientAsync(ClientData clientData)
    {
        Debug.LogWarning("check HandleClientAsync");
        string clientMsg;
        // int clientCount;

        while (clientList.Count == 1)
        {
            await clientData.streamWriter.WriteLineAsync($"hello hello hello");
            await clientData.streamWriter.FlushAsync();

            clientMsg = await clientData.streamReader.ReadLineAsync();
            if (clientMsg.StartsWith("QUIT:") && clientMsg != null)
            {
                await clientData.streamWriter.WriteLineAsync($"  {clientData.devID}  -- QUIT SUCCESFULLY  ");
                await clientData.streamWriter.FlushAsync();

                break;
            }
        }
        Debug.LogWarning("CLIENT QUIT:" + clientData.devID);
    }

    public void KillAll()
    {
        Debug.LogWarning("Shutting Down...");

        lock (_lock)
        {
            if (clientList.Count > 0)
            {
                foreach (ClientData clientData in clientList)
                {   
                    clientData.Dispose();
                    clientList.Remove(clientData);
                }
            }
        }

        if (isServerRunning)
        {
            server.Stop();
            Debug.LogWarning("Server Stopped!");
            isServerRunning = false;
        }
    }

    void Start()
    {
        Task serverStart = Task.Run(async () => await StartServer());
        if (serverStart.IsFaulted)
        {
            serverStart.Wait(); 
        }
    }

    void FixedUpdate()
    {
        if (hand != null)
        {
            OVRSkeleton skeleton = hand.GetComponent<OVRSkeleton>();
            if (skeleton != null)
            {
                foreach (var bone in skeleton.Bones)
                {
                    bonePosition = bone.Transform.position;
                    boneRotation = bone.Transform.rotation;
                    boneId = bone.Id;
                }
            }
        }
    }

    void OnDestroy()
    {
        KillAll();
    }  
} 
