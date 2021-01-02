# Brightness-based-Localization-Using-An-IoT-Device
Localization using a light sensor on 2 TI cc2650 sensortags and various machine learning models.
Localization model can locate a laptop or other electronic devices with a screen using the sensor tag's light sensor (OPT3001).

 `light_sensor_client.py` sends 600 requests to a sensortag programmed with `udp-server.c` via a sensor tag programmed as an rpl-border router ([border-router code](https://github.com/iot-lab/contiki/tree/master/examples/ipv6/rpl-border-router)). The `udp-server` takes readings at 10Hz responding to each request with a single reading. The `light_sensor_client` then records this data to a csv file. In `sensor-tag-sample.py` the data is used to train machine learning models (logistic regression, svm, knn, random forest, decision tree) which can make a classification on real time data with high accuracy.

##Results
![](https://raw.githubusercontent.com/Jon-bon-Jono/Brightness-based-Localization-Using-An-IoT-Device/main/tuning_svm.png)
![](https://raw.githubusercontent.com/Jon-bon-Jono/Brightness-based-Localization-Using-An-IoT-Device/main/tuning_knn.png)
![](https://raw.githubusercontent.com/Jon-bon-Jono/Brightness-based-Localization-Using-An-IoT-Device/main/tuning_decision_tree.PNG)
![](https://raw.githubusercontent.com/Jon-bon-Jono/Brightness-based-Localization-Using-An-IoT-Device/main/tuning_random_forest.PNG)
![](https://raw.githubusercontent.com/Jon-bon-Jono/Brightness-based-Localization-Using-An-IoT-Device/main/classifier_performance.png)
