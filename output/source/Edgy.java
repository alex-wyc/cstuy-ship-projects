import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import processing.video.Capture; 
import java.util.Arrays; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class Edgy extends PApplet {




Capture cam;
float[] deltaX;
float[] deltaY;
float[] r;
float[] g;
float[] b;

float threshold = 130;

float[] matrixX = {
  -1, 0, 1, 
  -2, 0, 2, 
  -1, 0, 1
};

float[] matrixY = {
  -1, -2, -1, 
  0, 0, 0, 
  1, 2, 1
};

public void setup() {
  size(640, 480);
  cam = new Capture(this, 640, 480);
  cam.start();
}

public void draw() {
  if (cam.available() != true) {
    return;
  }
  cam.read();
  cam.loadPixels();
  r = new float[cam.pixels.length];
  g = new float[cam.pixels.length];
  b = new float[cam.pixels.length];
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      int loc = x + y * width;

      r[loc] = red(cam.pixels[loc]);
      g[loc] = green(cam.pixels[loc]);
      b[loc] = blue(cam.pixels[loc]);
    }
  }

  deltaX = new float[cam.pixels.length];
  deltaY = new float[cam.pixels.length];

  for (int y = 1; y < height - 1; y++) {
    for (int x = 1; x < width - 1; x++) {
      int loc = x + y * width;
      // delta R
      float[] currentMatrix = getSurroundings(r, x, y);
      float deltaXHere = dotProduct(matrixX, currentMatrix);
      float deltaYHere = dotProduct(matrixY, currentMatrix);
      deltaX[loc] += abs(deltaXHere);
      deltaY[loc] += abs(deltaYHere);
      // delta G
      currentMatrix = currentMatrix = getSurroundings(g, x, y);
      deltaXHere = dotProduct(matrixX, currentMatrix);
      deltaYHere = dotProduct(matrixY, currentMatrix);
      deltaX[loc] += abs(deltaXHere);
      deltaY[loc] += abs(deltaYHere);
      // deltaB
      currentMatrix = getSurroundings(b, x, y);
      deltaXHere = dotProduct(matrixX, currentMatrix);
      deltaYHere = dotProduct(matrixY, currentMatrix);
      deltaX[loc] += abs(deltaXHere);
      deltaY[loc] += abs(deltaYHere);
    }
  }

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      int loc = x + y * width;
      if (deltaX[loc] + deltaY[loc] > threshold) {
        cam.pixels[loc] = color(0, 0, 0);
      } else {
        cam.pixels[loc] = color(255, 255, 255);
      }
    }
  }

  cam.updatePixels();
  background(cam);
  fill(255, 0, 0);
  textSize(32);
  text("threshold = " + (int)threshold, 20, 50);
}

public float[] getSurroundings(float[] all, int x, int y) {
  return new float[]{
        all[x - 1 + (y - 1) * width], 
        all[x + (y - 1) * width], 
        all[x + 1 + (y - 1) * width], 
        all[x - 1 + y * width], 
        all[x + y * width], 
        all[x + 1 + y * width], 
        all[x - 1 + (y + 1) * width], 
        all[x + (y + 1) * width], 
        all[x + 1 + (y + 1) * width]
      };
}

public float dotProduct(float[] vector1, float[] vector2) {
  float result = 0;
  for (int i = 0 ; i < vector1.length ; i++) {
    result += vector1[i] * vector2[i];
  }
  return result;
}

public void keyTyped() {
    if (key=='u') {
        threshold = threshold + 1;
    }
    if (key == 'd') {
        threshold = threshold - 1;
    }
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "Edgy" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
