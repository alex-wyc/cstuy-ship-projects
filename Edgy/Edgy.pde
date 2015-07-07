import processing.video.Capture;
import java.util.Arrays;

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

void setup() {
  size(640, 480);
  cam = new Capture(this, 640, 480);
  cam.start();
}

void draw() {
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
      float[] currentMatrix = {
        r[x - 1 + (y - 1) * width], 
        r[x + (y - 1) * width], 
        r[x + 1 + (y - 1) * width], 
        r[x - 1 + y * width], 
        r[x + y * width], 
        r[x + 1 + y * width], 
        r[x - 1 + (y + 1) * width], 
        r[x + (y + 1) * width], 
        r[x + 1 + (y + 1) * width]
      };
      for (int i = 0; i < 9; i++) {
        deltaX[x + y * width] += matrixX[i] * currentMatrix[i];
        deltaY[x + y * width] += matrixY[i] * currentMatrix[i];
      }
      currentMatrix = new float[]{
        g[x - 1 + (y - 1) * width], 
        g[x + (y - 1) * width], 
        g[x + 1 + (y - 1) * width], 
        g[x - 1 + y * width], 
        g[x + y * width], 
        g[x + 1 + y * width], 
        g[x - 1 + (y + 1) * width], 
        g[x + (y + 1) * width], 
        g[x + 1 + (y + 1) * width]
      };
      for (int i = 0; i < 9; i++) {
        deltaX[x + y * width] += matrixX[i] * currentMatrix[i];
        deltaY[x + y * width] += matrixY[i] * currentMatrix[i];
      }
      currentMatrix = new float[]{
        b[x - 1 + (y - 1) * width], 
        b[x + (y - 1) * width], 
        b[x + 1 + (y - 1) * width], 
        b[x - 1 + y * width], 
        b[x + y * width], 
        b[x + 1 + y * width], 
        b[x - 1 + (y + 1) * width], 
        b[x + (y + 1) * width], 
        b[x + 1 + (y + 1) * width]
      };
      for (int i = 0; i < 9; i++) {
        deltaX[x + y * width] += matrixX[i] * currentMatrix[i];
        deltaY[x + y * width] += matrixY[i] * currentMatrix[i];
      }
    }
  }

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      int loc = x + y * width;
      if (abs(deltaX[loc]) + abs(deltaY[loc]) > threshold) {
        cam.pixels[loc] = color(0, 0, 0);
      } else {
        cam.pixels[loc] = color(255, 255, 255);
      }
    }
  }

  cam.updatePixels();
  background(cam);
}
