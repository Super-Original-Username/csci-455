package com.example.networkedtts;

import androidx.appcompat.app.AppCompatActivity;

import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Message;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Enumeration;

public class NetworkActivity extends AppCompatActivity implements View.OnClickListener{
    ServerSocket ss;
    Thread Thread1 = null;
    Thread Thread2 = null;
    Thread Thread3 = null;
    TTS tts;
    TextView piIP;
    TextView msgIn;
    public static String IP = "";
    public static final int PORT = 8080;

    Button pow;

    private PrintWriter output;
    private BufferedReader input;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_network);
        piIP = findViewById(R.id.ip_box);
        msgIn = findViewById(R.id.msg_box);
        try{
            IP = getLocalIpAddress();
        }catch(UnknownHostException e){
            e.printStackTrace();
        }

        pow = findViewById(R.id.on_button);
        pow.setOnClickListener(this);
        Button locip = (Button)findViewById(R.id.locip_but);
        Button pcip = (Button)findViewById(R.id.pcip_but);
        locip.setOnClickListener(this);
        pcip.setOnClickListener(this);
    }


    private String getLocalIpAddress() throws UnknownHostException {
        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        assert wifiManager != null;
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int ipInt = wifiInfo.getIpAddress();
        return InetAddress.getByAddress(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(ipInt).array()).getHostAddress();
    }


    public static String getIpAddress() {
        String ipAddress = "Unable to Fetch IP..";
        try {
            Enumeration en;
            en = NetworkInterface.getNetworkInterfaces();
            while ( en.hasMoreElements()) {
                NetworkInterface intf = (NetworkInterface)en.nextElement();
                for (Enumeration enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = (InetAddress)enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress()&&inetAddress instanceof Inet4Address) {
                        ipAddress=inetAddress.getHostAddress().toString();
                        return ipAddress;
                    }
                }
            }
        } catch (SocketException ex) {
            ex.printStackTrace();
        }
        return ipAddress;
    }


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

    public void onClick(View v){
        String temp = "unitialized";
        switch (v.getId()){

            case R.id.on_button:
                String oSock =(String) piIP.getText();
                Thread1 = new Thread(new Thread1());
                Thread1.start();

                Toast.makeText(this, "talk", Toast.LENGTH_SHORT).show();
                //String input = msgText.getText().toString();
                Message sendMsg = tts.handler.obtainMessage();
                Bundle b = new Bundle();
                b.putString("TT",oSock);
                sendMsg.setData(b);
                tts.handler.sendMessage(sendMsg);
                break;
            case R.id.locip_but:
                try {
                    temp = getLocalIpAddress();
                }catch(Exception ignored){}
                Toast.makeText(this, temp, Toast.LENGTH_SHORT).show();
                break;
            case R.id.pcip_but:
                temp = getIpAddress();
                Toast.makeText(this, temp, Toast.LENGTH_SHORT).show();
                break;
        }
    }


}
