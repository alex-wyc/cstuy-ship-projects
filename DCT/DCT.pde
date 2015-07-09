boolean transformed = false;

void setup() {
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

void draw() {

}

void keyTyped() {
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

void DCT() {
    loadPixels();
    for (int y = 0 ; y < height ; y++) {
        for (int x = 0 ; x < width ; x++) {
            float result = 0;
            float currentBrightness = brightness(pixels[x + y * width]);
            for (int i = 0 ; i < width ; i++) {
                int loc = i + y * width;
                result = result + currentBrightness * cos(PI * (i + 0.5) * x / width);
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
                result = result + currentBrightness * cos(PI * (i + 0.5) * y / width);
            }
            pixels[x + y * width] = color(result);
        }
    }

    println("done");

    updatePixels();
}
