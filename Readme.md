## Sensor Fault Detection

### Overview
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.

This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class indicates that the failure was caused by something else.

### Proposed Solution
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

### Tech Stack Used
1. Python
2. FastAPI
3. Machine learning algorithms
4. Docker
5. MongoDB
6. Github Actions
7. AWS Services - S3, ECR, EC2

### High Level Code Flow
![alt text](<flowcharts/01_Pipeline.png>)

#### Data Ingestion Component Flow
![alt text](<flowcharts/02_Data_Ingestion.png>)

#### Data Validation Component Flow
![alt text](<flowcharts/03_Data_Validation.png>)

#### Data Transformation Component Flow
![alt text](<flowcharts/04_Data_Transformation.png>)

#### Model Training Component Flow
![alt text](<flowcharts/05_Model_Training.png>)

#### Model Evaluation Component Flow
![alt text](<flowcharts/06_Model_Evaluation.png>)

#### Model Pusher Component Flow
![alt text](<flowcharts/07_Model_Pusher.png>)

## License

This project is licensed under the MIT License.
