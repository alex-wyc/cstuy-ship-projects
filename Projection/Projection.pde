import processing.video.*;
import java.util.*;
import java.io.*;

int projWidth = 640;
int projHeight = 480;

Capture cam;

PImage projection;

float[][] rectangle = new float[][] {
    {0, projHeight},
    {projWidth, projHeight},
    {projWidth, 0},
    {0, 0}
};

float[][] TM;

void setup() {
    size(1280, 480);
    cam = new Capture(this, 640, 480);
    cam.start();
    projection = createImage(projWidth, projHeight, RGB);
    updateTMatrix();

    //float[][] testMatrix1 = new float[][] {
    //    {2, -1, 0},
    //    {3, -5, 2},
    //    {1, 4, -2}
    //};
    //float[][] identity = new float[][] {
    //    {3, -2, 5},
    //    {0, -1, 6},
    //    {-4, 2, -1}
    //};
    //float[][] TM4 = inverseMatrix3x3(testMatrix1);

    //float[][] result = matrixProduct3x3(testMatrix1, TM4);
    //for (int i = 0 ; i < 3; i++) {
    //    println(Arrays.toString(result[i]));
    //}

    //float[][] TM2 = QMatrix(1, 2, 3, 4, 5, 7, 36, 78);
    //float[][] TM3 = {{1, 0, 1}, {0, 1, 1}, {0, 0, 1}};
    //result = matrixProduct3x3(TM2, TM3);
    //println("" + result[0][0] / result[2][0] + " " + result[1][0] / result[2][0]);
    //println("" + result[0][1] / result[2][1] + " " + result[1][1] / result[2][1]);
    //println("" + result[0][2] / result[2][2] + " " + result[1][2] / result[2][2]);

}

void draw() {
    if (cam.available() == false) {
        return;
    }
    cam.read();
    cam.loadPixels();
    projection.loadPixels();
    for (int y = 0 ; y < projection.height ; y++) {
        for (int x = 0 ; x < projection.width ; x++) {
            float[] posVec = new float[] {x, y, 1};
            float[] result = matrixProduct(TM, posVec);
            int resultX = round(result[0] / result[2]);
            if (resultX < 0) {
                resultX = cam.width - resultX;
            }
            resultX = resultX % cam.width;
            int resultY = round(result[1] / result[2]);
            if (resultY < 0) {
                resultY = cam.height - resultY;
            }
            resultY = resultY % cam.height;

            try {
                projection.pixels[x + y * projection.width] = cam.pixels[resultX + resultY * cam.width];
            } catch (Exception e) {
                println("(x, y)");
                println("(" + x + ", " + y + ")");
                println("(resultX, resultY)");
                println("(" + resultX + ", " + resultY + ")");
            }

        }
    }

    cam.updatePixels();
    projection.updatePixels();

    image(cam, 0, 0);
    image(projection, cam.width, 0);
    for (int i = 0; i < rectangle.length; i++) {
        int j = (i + 1) % rectangle.length;
        line (rectangle[i][0], rectangle[i][1], rectangle[j][0], rectangle[j][1]);
    }
}

int selected_point = 0;

void mousePressed() {
    int min_point = -1;
    float min_distance = 0;
    for (int i = 0; i < rectangle.length; i++) {
        float distance = (rectangle[i][0] - mouseX) * (rectangle[i][0] - mouseX) + (rectangle[i][1] - mouseY) * (rectangle[i][1] - mouseY);
        if (min_point == -1 || distance < min_distance) {
            min_point = i;
            min_distance = distance;
        }
    }
    selected_point = min_point;
}

void mouseDragged() {
    rectangle[selected_point][0] = mouseX;
    rectangle[selected_point][1] = mouseY;
    updateTMatrix();
}

void updateTMatrix() {
    TM = transformMatrix(0, projHeight,
                         projWidth, projHeight,
                         projWidth, 0,
                         0, 0,
                         rectangle[0][0], rectangle[0][1],
                         rectangle[1][0], rectangle[1][1],
                         rectangle[2][0], rectangle[2][1],
                         rectangle[3][0], rectangle[3][1]);
    //TM = inverseMatrix3x3(TM);
}

float dotProduct(float[] vector1, float[] vector2) {
    float result = 0;
    for (int i = 0 ; i < vector1.length ; i++) {
        result += vector1[i] * vector2[i];
    }
    return result;
}

float[] matrixProduct(float[][] matrix, float[] vector1) {
    float[] result = new float[matrix.length];
    for (int i = 0 ; i < matrix.length ; i++) {
        result[i] = dotProduct(matrix[i], vector1);
    }
    return result;
}

float[][] matrixProduct(float[][] matrix, float c) {
    float[][] result = new float[matrix.length][matrix[0].length];
    for (int i = 0 ; i < matrix.length ; i++) {
        for (int j = 0 ; j < matrix[0].length ; j++) {
            result[i][j] = matrix[i][j] * c;
        }
    }
    return result;
}

float[][] matrixProduct3x3(float[][] matrix1, float[][] matrix2) {
    float[][] result = new float[3][3];
    for (int i = 0 ; i < 3 ; i++) {
        for (int j = 0 ; j < 3 ; j++) {
            result[i][j] += matrix1[i][0] * matrix2[0][j] +
                            matrix1[i][1] * matrix2[1][j] +
                            matrix1[i][2] * matrix2[2][j];
        }
    }
    return result;
}

float[][] cofactor3x3(float[][] original) {
    return new float[][]{
        {
            original[1][1] * original[2][2] - original[1][2] * original[2][1],
            -1 * (original[1][0] * original[2][2] - original[1][2] * original[2][0]),
            original[1][0] * original[2][1] - original[1][1] * original[2][0]
        },
        {
            -1 * (original[0][1] * original[2][2] - original[0][2] * original[2][1]),
            original[0][0] * original[2][2] - original[0][2] * original[2][0],
            -1 * (original[0][0] * original[2][1] - original[0][1] * original[2][0])
        },
        {
            original[0][1] * original[1][2] - original[0][2] * original[1][1],
            -1 * (original[0][0] * original[1][2] - original[0][2] * original[1][0]),
            original[0][0] * original[1][1] - original[0][1] * original[1][0]
        }
    };
}

float[][] inverseMatrix3x3(float[][] original) {
    float[][] cofactor = cofactor3x3(original);
    float determinant = dotProduct(cofactor[0], original[0]);
    transpose(cofactor);
    return matrixProduct(cofactor, 1 / determinant);
}

void transpose(float[][] original) {
    for (int i = 0 ; i < original.length ; i++) {
        for (int j = i + 1 ; j < original[0].length ; j++) {
            float temp = original[i][j];
            original[i][j] = original[j][i];
            original[j][i] = temp;
        }
    }
}

float[][] QMatrix(float ax, float ay,
                  float bx, float by,
                  float cx, float cy,
                  float dx, float dy) {
    float[][] matrix1 = new float[][] {
        {ax, bx, cx},
        {ay, by, cy},
        {1, 1, 1}
    };
    float[] vector1 = new float[] {dx, dy, 1};
    float[] multipliers = matrixProduct(inverseMatrix3x3(matrix1), vector1);
    return new float[][] {
        {multipliers[0] * ax, multipliers[1] * bx, multipliers[2] * cx},
        {multipliers[0] * ay, multipliers[1] * by, multipliers[2] * cy},
        {multipliers[0], multipliers[1], multipliers[2]}
    };
}

float[][] transformMatrix(float aix, float aiy,
                          float bix, float biy,
                          float cix, float ciy,
                          float dix, float diy,
                          float afx, float afy,
                          float bfx, float bfy,
                          float cfx, float cfy,
                          float dfx, float dfy) {

    float[][] Q2 = QMatrix(afx, afy,
                           bfx, bfy,
                           cfx, cfy,
                           dfx, dfy);
    float[][] Q1Inv = inverseMatrix3x3(QMatrix(aix, aiy,
                                               bix, biy,
                                               cix, ciy,
                                               dix, diy));
    float[][] TMatrix = matrixProduct3x3(Q2, Q1Inv);
    return TMatrix;
}
