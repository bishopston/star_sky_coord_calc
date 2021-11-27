import sys
from datetime import datetime, timedelta

def vegaLatLongCalc(t):
	"""
	Function to calculate exact latitude, longitude on earth which have star Vega at zenith
	dayTimePeriod = time period of one full sun circle above earth
	starPeriod = timedelta(hours = 23, minutes = 56, seconds = 4.0916) / time period of one full star circle above earth
	starDailyDriftDegrees = angle in degrees a star drifts compared to sun within a dayTimePeriod
	starHourlyDegrees = angle in degrees star moves in one hour
	vegaDeclination = declination of star Vega in decimal format (+38° 47′ 01.3″)
	vegaRA = right ascension of star Vega in degrees (18h 36m 56.34s)
	degreesLongPerHour = hourly angle in degrees of right ascension
	vernalEquinox = timestamp of Vernal Equinox in year 2019 (20/3/2019 22:08:00)
	vernalEquinoxLongRef = longitude corresponding to right ascension 00h 00m 00.00s on Vernal Equinox
	vegaLongStart = Vega longitude on Vernal Equinox in year 2019
	vegaLongDrift = drift in Vega longitude corresponding to days as per user input
	vegaLongEndA = Vega longitude taking into account drift as calculated by vegaLongDrift
	vegaLongEndB = Vega longitude taking into account drift corresponding to hours as per user input
	"+" declares eastward movement, "-" declares westward movement
	"""
	dayTimePeriod = timedelta(hours = 24, minutes = 0, seconds = 0)

	starDailyDriftDegrees = 0.9825

	starHourlyDegrees = 15.0409

	vegaDeclination = 38.7837

	vegaRA = 18.616
	
	degreesLongPerHour = 15
	
	vernalEquinox = datetime(2019, 3, 20, 22, 8, 00)
	
	vernalEquinoxLongRef = -150.25

	vegaLongStart = vernalEquinoxLongRef + vegaRA * degreesLongPerHour

	if vegaLongStart > 180:
		vegaLongStart -= 360


	try:
		_t = datetime.strptime(t, "%d/%m/%Y %H:%M:%S")

		tDelta = _t - vernalEquinox

		vegaLongDrift = (abs(tDelta.days) % 365.2425) * starDailyDriftDegrees
		
		if tDelta > timedelta(days = 0, hours = 0, minutes = 0, seconds = 0):

			vegaLongEndA = vegaLongStart - vegaLongDrift

			if vegaLongEndA < -180:
				vegaLongEndA += 360
			elif vegaLongEndA > 180:
				vegaLongEndA -= 360
				
			vegaLongEndB = vegaLongEndA - ((float((tDelta % dayTimePeriod).total_seconds()/3600)) * starHourlyDegrees)

			if vegaLongEndB < -180:
				vegaLongEndB += 360
			elif vegaLongEndB > 180:
				vegaLongEndB -= 360
				
		else:
		
			vegaLongEndA = vegaLongStart + vegaLongDrift

			if vegaLongEndA < -180:
				vegaLongEndA += 360
			elif vegaLongEndA > 180:
				vegaLongEndA -= 360
				
			vegaLongEndB = vegaLongEndA - ((float((tDelta % dayTimePeriod).total_seconds()/3600)) * starHourlyDegrees)

			if vegaLongEndB < -180:
				vegaLongEndB += 360
			elif vegaLongEndB > 180:
				vegaLongEndB -= 360
		
		
		print("Vega is at lat: {lat}, long: {long}.".format(lat=vegaDeclination, long=round(vegaLongEndB, 4)))

	except:
		print(sys.exc_info()[1])
	
if __name__ == "__main__":
	timestamp = input("Enter calculation timestamp (UTC) in DD/MM/YYYY HH:MM:SS format:")
	vegaLatLongCalc(timestamp)
	print("Positive latitude refers to place above Equator while negative latitude refers to place below Equator")
	print("Positive longitude refers to place east of Greenwich while negative longitude refers to place west of Greenwich")
	