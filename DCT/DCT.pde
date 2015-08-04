boolean transformed = false;

float[][] r;
float[][] g;
float[][] b;

void setup() {
    size(300, 300);
    background(255);
    PImage img = loadImage("./DCT.jpg");
    img.resize(300, 300);
    image(img, 0, 0);
    updatePixels();
    r = new float[width][height];
    g = new float[width][height];
    b = new float[width][height];
}

void draw() {

}

void keyTyped() {
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

    if (key == 'h') {
        DCT();
        highPass(r, 80);
        highPass(g, 80);
        highPass(b, 80);
        invDCT();
   }

   if (key == 'l') {
        DCT();
        lowPass(r, 10);
        lowPass(g, 10);
        lowPass(b, 10);
        invDCT();
   }
   
   if (key == 's') {
     save("DCT.jpg");
   }
}

void DCT() {
    loadPixels();
    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            r[y][x] = map(red(pixels[x + y * width]), 0, 255, 0, 1);
            g[y][x] = map(green(pixels[x + y * width]), 0, 255, 0, 1);
            b[y][x] = map(blue(pixels[x + y * width]), 0, 255, 0, 1);
        }
    }

    r = DCTHelper(r);
    println("red done");
    g = DCTHelper(g);
    println("green done");
    b = DCTHelper(b);
    println("blue done");

    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            //float red = map(r[y][x], -width*height, width*height, 0, 255);
            //float green = map(g[y][x], -width*height, width*height, 0, 255);
            //float blue = map(b[y][x], -width*height, width*height, 0, 255);
            float red = map(log(r[y][x]), 0, log(5000), 0, 255);
            float green = map(log(g[y][x]), 0, log(5000), 0, 255);
            float blue = map(log(b[y][x]), 0, log(5000), 0, 255);
            pixels[x + y * width] = color(red, green, blue);
        }
    }
    updatePixels();
}

float[][] DCTHelper(float[][] input) {
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
                result += input[y][i] * cos(PI * (i + 0.5) * x / w);
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
                result += output1[i][x] * cos(PI * (i + 0.5) * y / h);
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

void invDCT() {
    loadPixels();
    r = invDCTHelper(r);
    println("red done");
    g = invDCTHelper(g);
    println("green done");
    b = invDCTHelper(b);
    println("blue done");

    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            float red = map(r[y][x], 0, 1, 0, 255);
            float green = map(g[y][x], 0, 1, 0, 255);
            float blue = map(b[y][x], 0, 1, 0, 255);
            pixels[x + y * width] = color(red, green, blue);
        }
    }
    updatePixels();
}

float[][] invDCTHelper(float[][] input) {
    int h = input.length;
    int w = input[0].length;
    float[] results = new float[h * w];
    // Y-direction
    float[][] output1 = new float[h][w];
    float[] newline = new float[h];
    for (int x = 0 ; x < w ; x++) {
        for (int y = 0 ; y < h ; y++) {
            float result = input[0][x] / h;
            for (int i = 1 ; i < h ; i++) {
                result += 2 * input[i][x] * cos(PI * i * (y + 0.5) / h) / h;
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
            float result = output1[y][0] / w;
            for (int i = 1 ; i < w ; i++) {
                result += 2 * output1[y][i] * cos(PI * i * (x + 0.5) / w) / w;
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

void highPass(float[][] arr, float r) {
    for (int y = 0 ; y < arr.length ; y++) {
        for (int x = 0 ; x < arr[0].length ; x++) {
            if (x == 0 && y == 0) {
                arr[y][x] = width * height / 2;
                continue;
            }
            if (x * x + y * y < r * r) {
                arr[y][x] = 0;
            }
        }
    }
}

void lowPass(float[][] arr, float r) {
    for (int y = 0 ; y < arr.length ; y++) {
        for (int x = 0 ; x < arr[0].length ; x++) {
            if (x * x + y * y > r * r) {
                arr[y][x] = 0;
            }
        }
    }
}
