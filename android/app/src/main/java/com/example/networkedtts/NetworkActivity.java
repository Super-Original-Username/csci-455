package com.example.networkedtts;

import androidx.appcompat.app.AppCompatActivity;

import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Message;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class NetworkActivity extends AppCompatActivity {
    ServerSocket ss;
    NetListener nl;
    NetSender ns;
    Thread listenThread = null;
    TTS tts;
    TextView piIP;
    TextView msgIn;
    public static String IP = "";
    public static final int PORT = 8080;

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

    }

    private String getLocalIpAddress() throws UnknownHostException {
        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        assert wifiManager ! = null;
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int ipInt = wifiInfo.getIpAddress();
        return InetAddress.getByAddress(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(ipInt).array()).getHostAddress();
    }




    public void onClick(View v){

        switch (v.getId()){

            case R.id.talkButton:
                Toast.makeText(this, "talk", Toast.LENGTH_SHORT).show();
                String input = msgText.getText().toString();
                Message sendMsg = tts.handler.obtainMessage();
                Bundle b = new Bundle();
                b.putString("TT",input);
                sendMsg.setData(b);
                tts.handler.sendMessage(sendMsg);
                break;

        }
    }


}
