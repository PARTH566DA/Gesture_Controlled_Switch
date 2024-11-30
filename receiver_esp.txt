#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>  // Include the ArduinoJson library

const char* ssid = "SSID";
const char* password = "PASSWORD";
const char* serverURL = "http://192.***.***.**:8000/get_prediction";

#define RELAY_PIN 2  // GPIO pin for relay control

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
}


void reconnectWiFi() {
  // Attempt to reconnect if Wi-Fi is disconnected
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi disconnected. Reconnecting...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nReconnected to Wi-Fi");
  }
}

void controlRelay(String command) {
  if (command == "CLOCKWISE") {
    digitalWrite(RELAY_PIN, HIGH);  // Turn relay on
    Serial.println("Relay ON: Current flowing");
  } else if (command == "ANTICLOCKWISE") {
    digitalWrite(RELAY_PIN, LOW);  // Turn relay off
    Serial.println("Relay OFF: No current flow");
  } else {
    // Invalid or undefined command
    Serial.println("Data not defined: No change to relay state");
  }
}

void fetchGestureFromServer() {
  reconnectWiFi();  // Ensure Wi-Fi is connected

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);

    int httpResponseCode = http.GET();

    // Check if the server connection is successful
    if (httpResponseCode > 0) {
      if (httpResponseCode == 200) {  // HTTP OK
        String payload = http.getString();

        if (payload.length() == 0) {
          // No data received
          Serial.println("No data received from the server");
          return;
        }

        Serial.print("Received gesture from server: ");
        Serial.println(payload);

        // Parse the JSON response
        DynamicJsonDocument doc(1024);
        DeserializationError error = deserializeJson(doc, payload);

        if (error) {
          Serial.print("Failed to parse JSON: ");
          Serial.println(error.c_str());
          Serial.println("Data not defined");
          return;
        }

        // Extract the prediction value
        if (doc.containsKey("prediction")) {
          String prediction = doc["prediction"].as<String>();
          controlRelay(prediction);
        } else {
          Serial.println("Data not defined: Missing 'prediction' field");
        }
      } else {
        // Server responded with an error code
        Serial.print("Server responded with error code: ");
        Serial.println(httpResponseCode);
        Serial.println("No data received from the server");
      }
    } else {
      // HTTP request failed
      Serial.print("Failed to connect to server: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
      Serial.println("No data received from the server");
    }
    http.end();
  } else {
    Serial.println("Wi-Fi not connected. Cannot reach server.");
  }
}

void loop() {
  // Fetch gesture from server continuously
  fetchGestureFromServer();
  delay(2048);  // Delay to control polling frequency
}