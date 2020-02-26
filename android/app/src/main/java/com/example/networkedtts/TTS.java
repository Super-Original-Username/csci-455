package com.example.networkedtts;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.speech.tts.TextToSpeech;
import android.speech.tts.Voice;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.util.Locale;

public class TTS extends Thread implements TextToSpeech.OnInitListener {

    private TextToSpeech tts;
    private Context context;
    public Handler handler;
    private String last;
    TTS(Context con){
        context = con;
        tts = new TextToSpeech(con,this);
        last = "c";
    }

    /* standard initialization function for the TTS*/
    public void onInit(int status){
        if(status == TextToSpeech.SUCCESS) {
            int result = tts.setLanguage(Locale.US); // ensures that the language of the TTS is set to US english

            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Toast.makeText(context, "Language or data not working", Toast.LENGTH_SHORT).show(); //uses a toast to throw the error to the mobile user that something is unsupported
            }
        }
    }

    /* This is the function that takes in a _unique_ string input, and makes the talk do*/
    public void makeTalkDo(String inString){
        if(last != inString){
            last = inString;
            if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP){
                tts.speak(inString,TextToSpeech.QUEUE_FLUSH,null,null);
            }else{
                tts.speak(inString,TextToSpeech.QUEUE_FLUSH,null); // this is the same as above, but different
            }
            while (tts.isSpeaking()){// This ensures that the phone is done speaking before anything else can be sent
                try{
                    Thread.sleep(200);
                }catch(Exception ignored){}
            }
        }
    }

    /* Runs the thread that handles messages and calls the TTS function */
    @SuppressLint("HandlerLeak")
    public void run(){
        Looper.prepare(); // Thread-safe infinite looping function start
        handler = new Handler(){ //handler. Handles messages from other threads
            public void handleMessage(Message msg){ //if there is a message from the calling thread, this gets called
                String response = msg.getData().getString("TT"); //grabs the message from the calling thread
                makeTalkDo(response); // calls makeTalkDo with the message grabbed in the previous step
            }
        };
        Looper.loop(); // 'end' of the loop. Signals that the loop must keep on looping
    }
}
