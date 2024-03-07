# SQLAlchemy-Challenge
UTSA Data Analytics Bootcamp SQLAlchemy challenge containing .sqlite files and SQL ORM script used to analyze and output the data to visual figures and an app.

------------------------------------------------------------------------------------------------------------------
SURFSUP

Inside the SQLAlchemy-Challenge Repository there is a Resources folder used to supply the hawaii_measurements.csv and hawaii_stations.csv that make up the hawaii.sqlite database that is used for analysis in the climate_analysis.ipynb file and for API creation with the app.py. 

------------------------------------------------------------------------------------------------------------------
climate_analysis.ipynb

The climate_analysis jupyter notebook takes creates an engine from the hawaii.sqlite file and opens a session to perform multiple analytical queries on the data. Queries include filtering climate data such as daily precipitation and temperature in hawaii based upon recordings made within in the past year and by recordings made by unique weather stations. The data is then converted to a pandas dataframe for data visualization of precipitation and temperature over the most recent year available.

------------------------------------------------------------------------------------------------------------------
app.py

The app.py file serves to create a server API by utilizing Flask and engine sessions from the hawaii.sqlite database. The app defines multiple routes including the homne route displaying all available routes and formatting notes for inputs, the precipitation route that outputs precipitaion recordings for every day in the most recent year, the stations route which outputs all stations in the database, the tobs route which displays dates and temperatures for all recordings in the past year of the most active station, and the start and start-end routes which take in user route date input in order to output the minimum, maximum, and average temperatures for the date ranges supplied based on start date and start and end date ranges.