# unpaved
Find unpaved roads or tracks in a county and export to KML file

## Disclaimer
This application is intended for informational purposes only. Users are responsible for adhering to local laws and regulations regarding outdoor activities and land use. We do not condone illegal activities or trespassing. Always ensure that you have the proper permissions and are aware of local laws before engaging in any activities on the tracks identified by this tool.

## Usage
I've been using this app to find areas to scout for riding locations. Some of the tracks are gated or restricted to offroad vehicles. I've found that adding this KML file to my Garmin allows me to create a new layer and find when I'm nearby the locations. I would avoid relying on this map solely to ride trails or expect the trails to be maintained or having through access. 
https://advroads-deokhbrtefcpywtncvnmzd.streamlit.app/

![image](https://github.com/stuy2005/advroads/assets/31675142/00682919-4f66-4129-96eb-85893b00a991)

## Contributing
Contributions to the Unpaved Track Finder are welcome. Please feel free to fork the repository, make improvements, and submit pull requests.

## Running the app locally
### Installation

To run the Unpaved Track Finder, you need to have Python installed on your machine along with some additional libraries.

### Requirements:
- Python 3.6+
- Streamlit
- Overpy
- SimpleKML
- GeoPy

#### Steps to Install:
1. Clone the repository or download the source code.
2. Install the required Python libraries using pip:
   ```bash
   pip install streamlit overpy simplekml geopy

### Steps to Run Locally To start the application:

- Navigate to the directory containing the app script.
- Run the command:
  ```bash
  streamlit run streamlit_app.py
- The application interface will open in your default web browser.
- Follow the prompts in the user interface to select a state and county, and then fetch roads based on the selected criteria.
- Download the generated KML file to view the identified roads in any application that supports KML files, such as Google Earth.
