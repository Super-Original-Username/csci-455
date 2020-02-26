package com.example.networkedtts;

import android.os.Bundle;
import android.os.Message;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class TalkActivity extends AppCompatActivity implements View.OnClickListener {
    EditText msgText;
    TTS tts;


    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_talk);
        msgText = (EditText) findViewById(R.id.tts_phrase);
        Button talkButton = (Button)findViewById(R.id.talkButton);
        talkButton.setOnClickListener(this);
        tts = new TTS(this);
        tts.start();
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
