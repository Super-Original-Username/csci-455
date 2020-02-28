package com.example.networkedtts;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutput;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Enumeration;

public class NetworkActivity extends AppCompatActivity implements View.OnClickListener {
    //ServerSocket ss;
    TTS tts;
    TextView piIP;
    TextView msgIn;
    TextView myIP;
    public static String IP = "";
    public static final int PORT = 8080;

    Button pow;

    //Server s;

    private PrintWriter output;
    private BufferedReader input;

    Socket sock;
    Listener listen;
    Sender send;

    ServerSocket servSock;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_network);
        piIP = findViewById(R.id.ip_box);
        msgIn = findViewById(R.id.msg_box);
        myIP = findViewById(R.id.loc_ip);
       try {
            servSock = new ServerSocket();
           IP = getLocalIpAddress();
           servSock.bind(new InetSocketAddress(IP,PORT));

        }catch (IOException e){}
        tts = new TTS(this);
        tts.start();
        pow = findViewById(R.id.on_button);
        pow.setOnClickListener(this);
        try {
            myIP.setText(IP);

            Toast.makeText(this, servSock.getLocalSocketAddress().toString(), Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
        }
        /*
        Button locip = (Button) findViewById(R.id.locip_but);
        Button pcip = (Button) findViewById(R.id.pcip_but);
        locip.setOnClickListener(this);
        pcip.setOnClickListener(this);*/
    }

    /*Self- explanatory. Grabs IP, which is mostly just used for the app interface*/
    private String getLocalIpAddress() throws UnknownHostException {
        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        assert wifiManager != null;
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int ipInt = wifiInfo.getIpAddress();
        return InetAddress.getByAddress(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(ipInt).array()).getHostAddress();
    }

/*
    public static String getIpAddress() {
        String ipAddress = "Unable to Fetch IP..";
        try {
            Enumeration en;
            en = NetworkInterface.getNetworkInterfaces();
            while (en.hasMoreElements()) {
                NetworkInterface intf = (NetworkInterface) en.nextElement();
                for (Enumeration enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements(); ) {
                    InetAddress inetAddress = (InetAddress) enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && inetAddress instanceof Inet4Address) {
                        ipAddress = inetAddress.getHostAddress().toString();
                        return ipAddress;
                    }
                }
            }
        } catch (SocketException ex) {
            ex.printStackTrace();
        }
        return ipAddress;
    }
*/

    public void onClick(View v) {
        String temp = "unitialized";
        switch (v.getId()) {
            case R.id.on_button:
                //String oSock = (String) piIP.getText();
                //initializeServer();
                Thread st = new Thread(new ServThread());
                st.start();
                //s.start();
                break;
            /*
            case R.id.locip_but:
                try {
                    temp = getLocalIpAddress();
                } catch (Exception ignored) {
                }
                Toast.makeText(this, temp, Toast.LENGTH_SHORT).show();
                break;
            case R.id.pcip_but:
                temp = getIpAddress();
                Toast.makeText(this, temp, Toast.LENGTH_SHORT).show();
                break;*/
        }
    }

    void initializeServer() {
            try {
                sock = servSock.accept();
                Toast.makeText(this, sock.getInetAddress() + "connected", Toast.LENGTH_SHORT).show();
                listen = new Listener(sock);
                //send = new Sender(sock);
            } catch (IOException e) {
                e.printStackTrace();
            }
    }

    private class ServThread implements Runnable{
        public void run(){
            //try{
              //  servSock = new ServerSocket(PORT);
                //boolean con = false;
                //while(!con) {
                    try {
                        sock = servSock.accept();
                    }catch(Exception e){e.printStackTrace();}
                //}
                //Toast.makeText(this, sock.getInetAddress() + "connected", Toast.LENGTH_SHORT).show();
                listen = new Listener(sock);
                listen.start();

       // }catch(Exception e){
        //        Log.v("big","failed to initialize server socket");}
        }
    }


    private class Listener extends Thread {
        //Handler handler;
        Socket sock;
        Listener(Socket socket) {
            sock = socket;
        }

        public void run(){
            //Looper.prepare(); // Thread-safe infinite looping function start
            try {
                DataInputStream inFromClient = new DataInputStream(sock.getInputStream());
                while (true) {
                    String lastFromClient = "";
                    String newFromClient = "";
                    newFromClient = inFromClient.readLine();
                    if (!lastFromClient.equals(newFromClient)) {
                        lastFromClient = newFromClient;
                        msgIn.setText(lastFromClient);
                        speak(lastFromClient);
                    }
                }
            }catch (IOException e){}
            //Looper.loop(); // 'end' of the loop. Signals that the loop must keep on looping
        }

        public void speak(String toSay) {
            Message sendMsg = tts.handler.obtainMessage();
            Bundle b = new Bundle();
            b.putString("TT", toSay);
            sendMsg.setData(b);
            tts.handler.sendMessage(sendMsg);
        }
    }

    private class Sender extends Thread {
        Handler handler;
        DataOutputStream dOut;
        String msg;

        Sender(Socket sock, String message) {
            Socket socket = sock;
            msg = message;
            try {
                dOut = new DataOutputStream(sock.getOutputStream());
            } catch (IOException e) {
            }
        }


        public void run() {
            //Looper.prepare(); // Thread-safe infinite looping function start
            //handler = new Handler(){ //handler. Handles messages from other threads
            //public void handleMessage(Message msg){ //if there is a message from the calling thread, this gets called
            //String response = msg.getData().getString("TT"); //grabs the message from the calling thread
            try {
                dOut.writeByte(1);
                dOut.writeUTF(msg); // calls makeTalkDo with the message grabbed in the previous step
            } catch (IOException e) {
            }
        }

            //Looper.loop(); // 'end' of the loop. Signals that the loop must keep on looping
    }
}


/*
    class ListServ extends Thread {
        ListServ() {

        }

        /* Runs the thread that handles messages and calls the TTS function/
        @SuppressLint("HandlerLeak")
        public void run() {
            Looper.prepare(); // Thread-safe infinite looping function start
            handler = new Handler() { //handler. Handles messages from other threads
                public void handleMessage(Message msg) { //if there is a message from the calling thread, this gets called
                    String response = msg.getData().getString("TT"); //grabs the message from the calling thread
                    makeTalkDo(response); // calls makeTalkDo with the message grabbed in the previous step
                }
            };
            Looper.loop(); // 'end' of the loop. Signals that the loop must keep on looping
        }
    }

    class SendServ extends Thread {
        SendServ() {

        }

        /* Runs the thread that handles messages and calls the TTS function/
        @SuppressLint("HandlerLeak")
        public void run() {
            Looper.prepare(); // Thread-safe infinite looping function start
            handler = new Handler() { //handler. Handles messages from other threads
                public void handleMessage(Message msg) { //if there is a message from the calling thread, this gets called
                    String response = msg.getData().getString("TT"); //grabs the message from the calling thread
                    makeTalkDo(response); // calls makeTalkDo with the message grabbed in the previous step
                }
            };
            Looper.loop(); // 'end' of the loop. Signals that the loop must keep on looping
        }
    }
}
*/
/*
class Thread1 implements Runnable {
    @Override
    public void run() {
        Socket socket;
        try {
            ServerSocket serverSocket = new ServerSocket(PORT);
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    //piIP.setText("Not connected");
                    //piIP.setText("IP: " + IP);
                    //tvPort.setText("Port: " + String.valueOf(SERVER_PORT));
                }
            });
            try {
                socket = serverSocket.accept();
                output = new PrintWriter(socket.getOutputStream());
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        msgIn.setText("Connected\n");
                    }
                });
                new Thread(new Thread2()).start();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

private class Thread2 implements Runnable {
    @Override
    public void run() {
        while (true) {
            try {
                final String message = input.readLine();
                if (message != null) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            msgIn.append("client:" + message + "\n");
                        }
                    });
                } else {
                    Thread1 = new Thread(new Thread1());
                    Thread1.start();
                    return;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

class Thread3 implements Runnable {
    private String message;

    Thread3(String message) {
        this.message = message;
    }

    @Override
    public void run() {
        output.write(message);
        output.flush();
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                //tvMessages.append("server: " + message + "\n");
                //etMessage.setText("");
            }
        });
    }

}
*/

