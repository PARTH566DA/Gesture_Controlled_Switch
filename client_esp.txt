#include <Wire.h>
#include <MPU6050.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Wi-Fi credentials
const char* ssid = "SSID";
const char* password = "PASSWORD";
const char* serverUrl = "http://192.***.**.**:8000/predict";

MPU6050 mpu;

float accelX[128], accelY[128], accelZ[128];
float gyroX[128], gyroY[128], gyroZ[128];
int dataCount = 0;
bool collectingData = false;

// Function prototypes
float calculateMean(float* data, int size);
float calculateStd(float* data, int size);
float calculateEnergy(float* data, int size);
float Max_value(float* data, int size);
float calculateSMA(float* x, float* y, float* z, int size);
float calculateIQR(float* data, int size);
float calculateSkewness(float* data, int size);
float computeKurtosis(float* data, int size);
float calculateMin(float* data, int size);
float calculateMAD(float* data, int size);
float calculateCorrelation(float* data1, float* data2, int size);

void setup() {
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    int wifiTimeout = 20;
    int attempt = 0;
    while (WiFi.status() != WL_CONNECTED && attempt < wifiTimeout) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
        attempt++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("Connected to WiFi");
    } else {
        Serial.println("Failed to connect to WiFi");
    }

    // Initialize I2C and MPU6050
    Wire.begin(21, 22);
    mpu.initialize();
    if (!mpu.testConnection()) {
        Serial.println("MPU6050 connection failed");
        while (1);
    }
    Serial.println("MPU6050 initialized successfully");
}

void loop() {
    collectingData = true;
  
    // If data collection is active
    if (collectingData) {
        collectData();
    }

    // If enough data is collected and data collection is inactive, send to server
    if (!collectingData && dataCount >= 128) {
        sendToServer();
        dataCount = 0;
    }

    delay(10);
}

void collectData() {
    // Read MPU6050 data
    int16_t rawAx, rawAy, rawAz;
    int16_t rawGx, rawGy, rawGz;
    mpu.getMotion6(&rawAx, &rawAy, &rawAz, &rawGx, &rawGy, &rawGz);

    // Store scaled values in arrays
    accelX[dataCount] = rawAx / 16384.0;
    accelY[dataCount] = rawAy / 16384.0;
    accelZ[dataCount] = rawAz / 16384.0;
    gyroX[dataCount] = rawGx / 131.0;
    gyroY[dataCount] = rawGy / 131.0;
    gyroZ[dataCount] = rawGz / 131.0;

    dataCount++;

    // Stop data collection if enough data is collected
    if (dataCount >= 128) {
        collectingData = false;
        Serial.println("128 data points collected. Ready to send.");
    }

    delay(16);
}

void sendToServer() {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Calculate features
    float meanXA = calculateMean(accelX, 128);
    float stdXA = calculateStd(accelX, 128);
    float energyXA = calculateEnergy(accelX, 128);
    float maxXA = Max_value(accelX, 128);
    float SMA_XA = calculateSMA(accelX, accelY, accelZ, 128);
    float iqrXA = calculateIQR(accelX, 128);
    float skewnessXA = calculateSkewness(accelX, 128);
    float kurtosisXA = computeKurtosis(accelX, 128);
    float minXA = calculateMin(accelX, 128);
    float madXA = calculateMAD(accelX, 128);
    float correlationXYA = calculateCorrelation(accelX, accelY, 128);

    float meanXG = calculateMean(gyroX, 128);
    float stdXG = calculateStd(gyroX, 128);
    float energyXG = calculateEnergy(gyroX, 128);
    float maxXG = Max_value(gyroX, 128);
    float SMA_XG = calculateSMA(gyroX, gyroY, gyroZ, 128);
    float iqrXG = calculateIQR(gyroX, 128);
    float skewnessXG = calculateSkewness(gyroX, 128);
    float kurtosisXG = computeKurtosis(gyroX, 128);
    float minXG = calculateMin(gyroX, 128);
    float madXG = calculateMAD(gyroX, 128);
    float correlationXYG = calculateCorrelation(gyroX, gyroY, 128);

    // Y axis calculations
    float meanYA = calculateMean(accelY, 128);
    float stdYA = calculateStd(accelY, 128);
    float energyYA = calculateEnergy(accelY, 128);
    float maxYA = Max_value(accelY, 128);
    float SMA_YA = calculateSMA(accelX, accelY, accelZ, 128);
    float iqrYA = calculateIQR(accelY, 128);
    float skewnessYA = calculateSkewness(accelY, 128);
    float kurtosisYA = computeKurtosis(accelY, 128);
    float minYA = calculateMin(accelY, 128);
    float madYA = calculateMAD(accelY, 128);
    float correlationYZA = calculateCorrelation(accelY, accelZ, 128);

    float meanYG = calculateMean(gyroY, 128);
    float stdYG = calculateStd(gyroY, 128);
    float energyYG = calculateEnergy(gyroY, 128);
    float maxYG = Max_value(gyroY, 128);
    float SMA_YG = calculateSMA(gyroX, gyroY, gyroZ, 128);
    float iqrYG = calculateIQR(gyroY, 128);
    float skewnessYG = calculateSkewness(gyroY, 128);
    float kurtosisYG = computeKurtosis(gyroY, 128);
    float minYG = calculateMin(gyroY, 128);
    float madYG = calculateMAD(gyroY, 128);
    float correlationYZG = calculateCorrelation(gyroY, gyroZ, 128);

    // Z axis calculations
    float meanZA = calculateMean(accelZ, 128);
    float stdZA = calculateStd(accelZ, 128);
    float energyZA = calculateEnergy(accelZ, 128);
    float maxZA = Max_value(accelZ, 128);
    float SMA_ZA  = calculateSMA(accelX, accelY, accelZ, 128);
    float iqrZA = calculateIQR(accelZ, 128);
    float skewnessZA = calculateSkewness(accelZ, 128);
    float kurtosisZA = computeKurtosis(accelZ, 128);
    float minZA = calculateMin(accelZ, 128);
    float madZA = calculateMAD(accelZ, 128);
    float correlationZXA = calculateCorrelation(accelZ, accelX, 128);

    float meanZG = calculateMean(gyroZ, 128);
    float stdZG = calculateStd(gyroZ, 128);
    float energyZG = calculateEnergy(gyroZ, 128);
    float maxZG = Max_value(gyroZ, 128);
    float SMA_ZG = calculateSMA(gyroX, gyroY, gyroZ, 128);
    float iqrZG = calculateIQR(gyroZ, 128);
    float skewnessZG = calculateSkewness(gyroZ, 128);
    float kurtosisZG = computeKurtosis(gyroZ, 128);
    float minZG = calculateMin(gyroZ, 128);
    float madZG = calculateMAD(gyroZ, 128);
    float correlationZXG = calculateCorrelation(gyroZ, gyroX, 128);

    const size_t capacity = 2048;
    StaticJsonDocument<capacity> doc;

    // Populate JSON document with data in an array format
    JsonArray features = doc.createNestedArray("features");
    
    features.add(meanXA);
    features.add(stdXA);
    features.add(energyXA);
    features.add(maxXA);
    features.add(SMA_XA);
    features.add(iqrXA);
    features.add(skewnessXA);
    features.add(kurtosisXA);
    features.add(minXA);
    features.add(madXA);
    features.add(correlationXYA);

    features.add(meanXG);
    features.add(stdXG);
    features.add(energyXG);
    features.add(maxXG);
    features.add(SMA_XG);
    features.add(iqrXG);
    features.add(skewnessXG);
    features.add(kurtosisXG);
    features.add(minXG);
    features.add(madXG);
    features.add(correlationXYG);

    features.add(meanYA);
    features.add(stdYA);
    features.add(energyYA);
    features.add(maxYA);
    features.add(SMA_YA);
    features.add(iqrYA);
    features.add(skewnessYA);
    features.add(kurtosisYA);
    features.add(minYA);
    features.add(madYA);
    features.add(correlationYZA);

    features.add(meanYG);
    features.add(stdYG);
    features.add(energyYG);
    features.add(maxYG);
    features.add(SMA_YG);
    features.add(iqrYG);
    features.add(skewnessYG);
    features.add(kurtosisYG);
    features.add(minYG);
    features.add(madYG);
    features.add(correlationYZG);

    features.add(meanZA);
    features.add(stdZA);
    features.add(energyZA);
    features.add(maxZA);
    features.add(SMA_ZA);
    features.add(iqrZA);
    features.add(skewnessZA);
    features.add(kurtosisZA);
    features.add(minZA);
    features.add(madZA);
    features.add(correlationZXA);

    features.add(meanZG);
    features.add(stdZG);
    features.add(energyZG);
    features.add(maxZG);
    features.add(SMA_ZG);
    features.add(iqrZG);
    features.add(skewnessZG);
    features.add(kurtosisZG);
    features.add(minZG);
    features.add(madZG);
    features.add(correlationZXG);


    String requestBody;
    serializeJson(doc, requestBody);


    Serial.println("Sending JSON payload:");
    Serial.println(requestBody);

    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode <= 0) {
        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
        Serial.println(http.errorToString(httpResponseCode));
    }
    else{
      Serial.print("Hello");
    }


    http.end();

    // Reset dataCount and start collecting data again
    dataCount = 0;
    collectingData = true;
    Serial.println("Ready to collect new data set.");
}

float calculateMean(float data[], int length) {
    float sum = 0.0;
    for (int i = 0; i < length; i++) {
        sum += data[i];
    }
    return sum / length;
}

float calculateStd(float data[], int length) {
    float mean = calculateMean(data, length);
    float sumSquaredDiffs = 0.0;
    for (int i = 0; i < length; i++) {
        sumSquaredDiffs += pow(data[i] - mean, 2);
    }
    return sqrt(sumSquaredDiffs / length);
}

float calculateEnergy(float data[], int length) {
    float energy = 0.0;
    for (int i = 0; i < length; i++) {
        energy += pow(data[i], 2);
    }
    return energy / length;
}

float calculateCorrelation(float data1[], float data2[], int length) {
    float mean1 = calculateMean(data1, length);
    float mean2 = calculateMean(data2, length);
    float numerator = 0.0;
    float sumSqData1 = 0.0;
    float sumSqData2 = 0.0;

    for (int i = 0; i < length; i++) {
        numerator += (data1[i] - mean1) * (data2[i] - mean2);
        sumSqData1 += pow(data1[i] - mean1, 2);
        sumSqData2 += pow(data2[i] - mean2, 2);
    }

    return numerator / sqrt(sumSqData1 * sumSqData2);
}

float Max_value(float data[], int length){
    float Max=-9999;
    for(int i=0; i < length; i++){
        if(data[i] > Max){
            Max = data[i];
        }
    }
    return Max;
} 


float calculateSMA(float accelX[], float accelY[], float accelZ[], int length) {
    float sma = 0.0;
    for (int i = 0; i < length; i++) {
        sma += (abs(accelX[i]) + abs(accelY[i]) + abs(accelZ[i]));
    }
    return sma / length;
}

float calculateMedian(float data[], int length) {
    if (length % 2 == 0) {
        // If even, average the two middle elements
        return (data[length / 2 - 1] + data[length / 2]) / 2.0;
    } else {
        // If odd, return the middle element
        return data[length / 2];
    }
}

void bubbleSort(float data[], int length) {
    for (int i = 0; i < length - 1; i++) {
        for (int j = 0; j < length - i - 1; j++) {
            if (data[j] > data[j + 1]) {
                float temp = data[j];
                data[j] = data[j + 1];
                data[j + 1] = temp;
            }
        }
    }
}


float calculateIQR(float data[], int length) {
    // Sort the array
    bubbleSort(data,length);

    // Calculate Q1 and Q3
    float Q1, Q3;
    if (length % 2 == 0) {
        // If even, split data in half
        int mid = length / 2;
        Q1 = calculateMedian(data, mid);             // Median of lower half
        Q3 = calculateMedian(data + mid, mid);       // Median of upper half
    } else {
        // If odd, split excluding the middle element
        int mid = length / 2;
        Q1 = calculateMedian(data, mid);             // Median of lower half
        Q3 = calculateMedian(data + mid + 1, mid);   // Median of upper half
    }

    // Return the IQR
    return Q3 - Q1;
}


float calculateSkewness(float data[], int length) {
    float mean = calculateMean(data, length);
    float stdDev = calculateStd(data, length);  // Assuming calculateStd is available
    float sumCubedDiffs = 0.0;

    for (int i = 0; i < length; i++) {
        sumCubedDiffs += pow(data[i] - mean, 3);
    }

    return (sumCubedDiffs / length) / pow(stdDev, 3);
}


float computeKurtosis(float data[], int length) {
    float mean = calculateMean(data, length);
    float std = calculateStd(data, length);
    float sumFourthMoment = 0.0;

    for (int i = 0; i < length; i++) {
        sumFourthMoment += pow((data[i] - mean) / std, 4);
    }

    return sumFourthMoment / length - 3;
}


float calculateAngleBetweenVectors(float vec1[], float vec2[], int length) {
    float dotProduct = 0.0;
    float magnitudeVec1 = 0.0;
    float magnitudeVec2 = 0.0;

    // Calculate dot product and magnitudes of both vectors
    for (int i = 0; i < length; i++) {
        dotProduct += vec1[i] * vec2[i];
        magnitudeVec1 += pow(vec1[i], 2);
        magnitudeVec2 += pow(vec2[i], 2);
    }

    magnitudeVec1 = sqrt(magnitudeVec1);
    magnitudeVec2 = sqrt(magnitudeVec2);

    // Prevent division by zero
    if (magnitudeVec1 == 0 || magnitudeVec2 == 0) {
        return 0.0;
    }

    // Calculate the angle in radians and then convert to degrees
    float cosTheta = dotProduct / (magnitudeVec1 * magnitudeVec2);
    return acos(cosTheta) * (180.0 / PI); // Return angle in degrees
}

float calculateMeanFrequency(float frequencies[], float weights[], int length) {
    float weightedSum = 0.0;
    float weightSum = 0.0;

    for (int i = 0; i < length; i++) {
        weightedSum += frequencies[i] * weights[i];  // Sum of weighted frequencies
        weightSum += weights[i];                       // Sum of weights
    }

    // Avoid division by zero
    if (weightSum == 0) {
        return 0; // To prevent division by zero
    }

    return weightedSum / weightSum; // Return weighted average
}


float calculateEntropy(float data[], int length) {
    // Calculate probability distribution
    float histogram[256] = {0}; // Histogram for 256 values
    for (int i = 0; i < length; i++) {
        int index = (int)(data[i] * 128); // Scale to [0, 255]
        if (index >= 0 && index < 256) {
            histogram[index]++;
        }
    }

    // Normalize histogram to get probabilities
    for (int i = 0; i < 256; i++) {
        histogram[i] /= length;
    }

    // Calculate Shannon entropy
    float entropy = 0.0;
    for (int i = 0; i < 256; i++) {
        if (histogram[i] > 0) {
            entropy -= histogram[i] * log2(histogram[i]);
        }
    }

    return entropy; // Return the calculated entropy
}


float calculateMin(float data[], int length) {
    float Min = 9999; // Initialize with a large value
    for (int i = 0; i < length; i++) {
        if (data[i] < Min) {
            Min = data[i];
        }
    }
    return Min;
}

float calculateMAD(float data[], int length) {
    float mean = calculateMean(data, length);
    float *absoluteDeviations = (float*)malloc(length * sizeof(float));

    for (int i = 0; i < length; i++) {
        absoluteDeviations[i] = fabs(data[i] - mean);
    }

    float mad = calculateMedian(absoluteDeviations, length);
    free(absoluteDeviations); // Free allocated memory for absolute deviations
    return mad;
}