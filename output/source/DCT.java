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
    PImage img = loadImage("./image.png");
    img.resize(300, 300);
    background(img);
    updatePixels();
}

public void draw() {

}

public void keyTyped() {
    if (key == 't') {
        if (!(transformed)) {
            println("key pressed");
            DCT();
            println("transformed");
        }
        else {
            println("key pressed");
            invDCT();
            println("invertedBack");
        }
        transformed = !(transformed);
    }
}

public void DCT() {
    loadPixels();
    float[][] r = new float[width][height];
    float[][] g = new float[width][height];
    float[][] b = new float[width][height];
    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            r[y][x] = map(red(pixels[x + y * width]), 0, 255, 0, 1);
            g[y][x] = map(red(pixels[x + y * width]), 0, 255, 0, 1);
            b[y][x] = map(red(pixels[x + y * width]), 0, 255, 0, 1);
        }
    }

    r = DCTHelper(r);
    println("red done");
    g = DCTHelper(g);
    println("green done");
    b = DCTHelper(b);
    println("blue done");

    halfShift(r);
    halfShift(g);
    halfShift(b);

    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            float red = map(r[y][x], 0, 60771, 0, 255);
            float green = map(g[y][x], 0, 60771, 0, 255);
            float blue = map(b[y][x], 0, 60771, 0, 255);
            pixels[x + y * width] = color(red, green, blue);
        }
    }
    updatePixels();
}

public float[][] DCTHelper(float[][] input) {
    int h = input.length;
    int w = input[0].length;
    // X-direction
    float[] results = new float[h * w];
    float[][] output1 = new float[h][w];
    float[] newline = new float[w];
    for (int y = 0 ; y < h ; y++) {
        for (int x = 0 ; x < w ; x++) {
            float result = 0;
            for (int i = 0 ; i < w ; i++) {
                result += input[y][i] * cos(PI * (i + 0.5f) * x);
            }
            newline[x] = result;
        }
        for (int i = 0 ; i < w ; i++) {
            output1[y][i] = newline[i];
        }
    }
    // Y-direction
    float[][] output2 = new float[h][w];
    newline = new float[h];
    for (int x = 0 ; x < w ; x++) {
        for (int y = 0 ; y < h ; y++) {
            float result = 0;
            for (int i = 0 ; i < h ; i++) {
                result += output1[i][x] * cos(PI * (i + 0.5f) * y);
            }
            newline[y] = result;
            results[x + y * width] = result;
        }
        for (int i = 0 ; i < h ; i++) {
            output2[i][x] = newline[i];
        }
    }

    float maxVal = results[0];
    float minVal = results[0];
    for (int i = 0 ; i < results.length ; i++) {
        if (results[i] > maxVal) {
            maxVal = results[i];
        }
        if (results[i] < minVal) {
            minVal = results[i];
        }
    }
    println("Max Val: " + maxVal);
    println("Min Val: " + minVal);


    return output2;
}

public void invDCT() {
    loadPixels();
    float[][] r = new float[width][height];
    float[][] g = new float[width][height];
    float[][] b = new float[width][height];
    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            r[y][x] = map(red(pixels[x + y * width]), 0, 255, 0, 1);
            g[y][x] = map(red(pixels[x + y * width]), 0, 255, 0, 1);
            b[y][x] = map(red(pixels[x + y * width]), 0, 255, 0, 1);
        }
    }

    halfShift(r);
    halfShift(g);
    halfShift(b);

    r = invDCTHelper(r);
    println("red done");
    g = invDCTHelper(g);
    println("green done");
    b = invDCTHelper(b);
    println("blue done");

    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            float red = map(r[y][x], 11142.887f, 11143.486f, 0, 255);
            float green = map(g[y][x], 11142.887f, 11143.486f, 0, 255);
            float blue = map(b[y][x], 11142.887f, 11143.486f, 0, 255);
            pixels[x + y * width] = color(red, green, blue);
        }
    }
    updatePixels();
}

public float[][] invDCTHelper(float[][] input) {
    int h = input.length;
    int w = input[0].length;
    float[] results = new float[h * w];
    // Y-direction
    float[][] output1 = new float[h][w];
    float[] newline = new float[h];
    for (int x = 0 ; x < w ; x++) {
        for (int y = 0 ; y < h ; y++) {
            float result = input[0][x] / 2;
            for (int i = 1 ; i < h ; i++) {
                result += input[i][x] * cos(PI * i * (y + 0.5f));
            }
            newline[y] = result;
            //println(result);
        }
        for (int i = 0 ; i < h ; i++) {
            output1[i][x] = newline[i];
        }
    }

    // X-direction
    float[][] output2 = new float[h][w];
    newline = new float[w];
    for (int y = 0 ; y < h ; y++) {
        for (int x = 0 ; x < w ; x++) {
            float result = output1[y][0] / 2;
            for (int i = 1 ; i < w ; i++) {
                result += output1[y][i] * cos(PI * i * (x + 0.5f));
            }
            newline[x] = result;
            results[x + y * width] = result;
        }
        for (int i = 0 ; i < w ; i++) {
            output2[y][i] = newline[i];
        }
    }
    float maxVal = results[0];
    float minVal = results[0];
    for (int i = 0 ; i < results.length ; i++) {
        if (results[i] > maxVal) {
            maxVal = results[i];
        }
        if (results[i] < minVal) {
            minVal = results[i];
        }
    }
    println("Max Val: " + maxVal);
    println("Min Val: " + minVal);

    return output2;
}


public void halfShift(float[][] data) {
    int w = data[0].length;
    int h = data.length;
    for (int y = 0 ; y < h / 2 ; y++) {
        for (int x = 0 ; x < w ; x++) {
            int xp = (x + w / 2) % w;
            int yp = y + h / 2;
            float temp;
            temp = data[y][x];
            data[y][x] = data[yp][xp];
            data[yp][xp] = temp;
        }
    }
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
