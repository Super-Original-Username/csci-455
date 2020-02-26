package com.example.networkedtts;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button talkButton = (Button)findViewById(R.id.talkMode);
        talkButton.setOnClickListener(this);
    }

    public void onClick(View v){
        Toast.makeText(this, "OnClick called", Toast.LENGTH_SHORT).show();
        switch (v.getId()){

            case R.id.talkMode:
                talk();
                break;
            case R.id.ipButton:
                getIP();
                break;


        }
    }

    public void talk(){
        Log.v("**Big**","Talk pressed");
        Intent talkTalk = new Intent(this,TalkActivity.class);
        try {
            startActivity(talkTalk);
        }catch(Exception e){
            Log.v("Scary",e.toString());
        }
    }

    public void getIP(){
        //TODO: implement the IP grabbing code from the tutorialspoint article linked on d2l
    }
}
