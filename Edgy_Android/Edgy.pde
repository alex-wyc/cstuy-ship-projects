import java.util.Arrays;
import android.content.Context;
import android.hardware.Camera;
import android.hardware.Camera.PreviewCallback;
import android.view.SurfaceHolder;
import android.view.SurfaceHolder.Callback;
import android.view.SurfaceView;
import android.view.Surface;

CameraSurfaceView gCamSurfView;
PImage gBuffer;
float[] deltaX;
float[] deltaY;
float[] brightness;

float threshold = 50;

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
    size(displayWidth, displayHeight);
}

void draw() {
}

void onResume() {
    super.onResume();
    orientation(LANDSCAPE);
    gCamSurfView = new CameraSurfaceView(this.getApplicationContext());
}

// Taken from 
class CameraSurfaceView extends SurfaceView implements SurfaceHolder.Callback, Camera.PreviewCallback {
  
    // Object that accesses the camera, and updates our image data
    // Using ideas pulled from 'Android Wireless Application Development', page 340
    SurfaceHolder mHolder;
    Camera cam = null;
    Camera.Size prevSize;
  
    // SurfaceView Constructor:  : ---------------------------------------------------
    CameraSurfaceView(Context context) {
        super(context);
        // Processing PApplets come with their own SurfaceView object which can be accessed
        // directly via its object name, 'surfaceView', or via the below function:
        // mHolder = surfaceView.getHolder();
        mHolder = getSurfaceHolder();
        // Add this object as a callback:
        mHolder.addCallback(this);
    }
  
    // SurfaceHolder.Callback stuff: ------------------------------------------------------
    void surfaceCreated (SurfaceHolder holder) {
        // When the SurfaceHolder is created, create our camera, and register our
        // camera's preview callback, which will fire on each frame of preview:
        cam = Camera.open();
        cam.setPreviewCallback(this);
        Camera.Parameters parameters = cam.getParameters();
        // Find our preview size, and init our global PImage:
        prevSize = parameters.getPreviewSize();
        gBuffer = createImage(prevSize.width, prevSize.height, RGB);
    }
  
    void surfaceChanged(SurfaceHolder holder,  int format,  int w,  int h) {
        // Start our camera previewing:
        cam.startPreview();
    }
  
    void surfaceDestroyed (SurfaceHolder holder) {
        // Give the cam back to the phone:
        cam.stopPreview();
        cam.release();
        cam = null;     
    }
  
     //  Camera.PreviewCallback stuff: ------------------------------------------------------
     void onPreviewFrame(byte[] data, Camera cam) {
         // This is called every frame of the preview.  Update our global PImage.
         gBuffer.loadPixels();
         // Decode our camera byte data into RGB data:
  
         decodeYUV420SP(gBuffer.pixels, data, prevSize.width, prevSize.height);

         // EDGE DETECTION
         brightness = new float[gBuffer.pixels.length];
         for (int y = 0; y < gBuffer.height; y++) {
             for (int x = 0; x < gBuffer.width; x++) {
                 int loc = x + y * gBuffer.width;
                 brightness[loc] = brightness(gBuffer.pixels[loc]);
             }
         }
  
         deltaX = new float[gBuffer.pixels.length];
         deltaY = new float[gBuffer.pixels.length];
  
         for (int y = 1; y < gBuffer.height - 1; y++) {
             for (int x = 1; x < gBuffer.width - 1; x++) {
                 float[] currentMatrix = {
                     brightness[x - 1 + (y - 1) * gBuffer.width], 
                     brightness[x + (y - 1) * gBuffer.width], 
                     brightness[x + 1 + (y - 1) * gBuffer.width], 
                     brightness[x - 1 + y * gBuffer.width], 
                     brightness[x + y * gBuffer.width], 
                     brightness[x + 1 + y * gBuffer.width], 
                     brightness[x - 1 + (y + 1) * gBuffer.width], 
                     brightness[x + (y + 1) * gBuffer.width], 
                     brightness[x + 1 + (y + 1) * gBuffer.width]
                 };
                 for (int i = 0; i < 9; i++) {
                     deltaX[x + y * gBuffer.width] += matrixX[i] * currentMatrix[i];
                     deltaY[x + y * gBuffer.width] += matrixY[i] * currentMatrix[i];
                 }
             }
         }
  
         for (int y = 0; y < gBuffer.height; y++) {
             for (int x = 0; x < gBuffer.width; x++) {
                 int loc = x + y * gBuffer.width;
                 if (abs(deltaX[loc]) + abs(deltaY[loc]) > threshold) {
                     gBuffer.pixels[loc] = color(0, 0, 0);
                 }
                 else {
                     gBuffer.pixels[loc] = color(255, 255, 255);
                 }
             }
         }
   
         gBuffer.updatePixels();
   
         // Draw to screen:
   
         image(gBuffer,  0,  0);   
    }
  
    //  Byte decoder : ---------------------------------------------------------------------
  
    void decodeYUV420SP(int[] rgb,  byte[] yuv420sp,  int width,  int height) {
  
        // Pulled directly from:
        // http://ketai.googlecode.com/svn/trunk/ketai/src/edu/uic/ketai/inputService/KetaiCamera.java
  
        final int frameSize = width * height;
        for  (int j = 0, yp = 0; j < height; j++) {
            int uvp = frameSize + (j >> 1) * width, u = 0, v = 0;
            for  (int i = 0; i < width; i++, yp++) {
                int y = (0xff & ((int) yuv420sp[yp])) - 16;
                if  (y < 0) {
                    y = 0;
                }
                if  ((i & 1) == 0) {
                    v = (0xff & yuv420sp[uvp++]) - 128;
                    u = (0xff & yuv420sp[uvp++]) - 128;         
                }       
  
                int y1192 = 1192 * y;
                int r = (y1192 + 1634 * v);
                int g = (y1192 - 833 * v - 400 * u);
                int b = (y1192 + 2066 * u);
  
                if  (r < 0) {
                    r = 0;
                }
                else if (r > 262143) {
                    r = 262143;
                }
                if  (g < 0) {
                    g = 0;
                }
                else if (g > 262143) {
                    g = 262143;
                }
                if  (b < 0) {
                    b = 0;
                }
                else if (b > 262143) {
                    b = 262143;
                }
  
                rgb[yp] = 0xff000000 | ((r << 6) & 0xff0000) | ((g >> 2) &0xff00) | ((b >> 10) & 0xff);
            }  
        }   
    }
}
