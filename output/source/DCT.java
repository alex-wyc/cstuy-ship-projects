import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class DCT extends PApplet {

boolean transformed = false;

public void setup() {
    size(300, 300);
    PImage superoctocat = loadImage("./superoctocat.jpg");
    superoctocat.resize(300, 300);
    background(superoctocat);
    loadPixels();
    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            int loc = x + y * width;
            pixels[loc] = color(brightness(pixels[loc]));
        }
    }
    updatePixels();
}

public void draw() {

}

public void keyTyped() {
    if (key == 't') {
        println("typed");
        DCT();
        println("transformed");
/*        if (!(transformed)) {
            DCT();
            println("transformed");
        }
        else {
            //InvDCT();
        }
        //transformed = !(transformed);*/
    }
}

public void DCT() {
    loadPixels();
    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            float result = 0;
            float currentBrightness = brightness(pixels[x + y * width]);
            for (int i = 0 ; i < width ; i++) {
                int loc = i + y * width;
                result = result + currentBrightness * cos(PI * (i + 0.5f) * x / width);
            }
            pixels[x + y * width] = color(result);
        }
    }

    println("one direction complete");

    for (int x = 0 ; x < width ; x++) {
        for (int y = 0 ; y < height ; y++) {
            float result = 0;
            float currentBrightness = brightness(pixels[x + y * width]);
            for (int i = 0 ; i < height ; i++) {
                int loc = x + i * height;
                result = result + currentBrightness * cos(PI * (i + 0.5f) * y / width);
            }
            pixels[x + y * width] = color(result);
        }
    }

    println("done");

    updatePixels();
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "DCT" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
