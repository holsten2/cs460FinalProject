# Statistical Network Analysis

### Netstat.py

Configuration Dependencies:<br>
	**speedtestcli** -- https://github.com/sivel/speedtest-cli <br>
	**pyplot** -- http://matplotlib.org/api/pyplot_api.html <br>

Usage: netstat.py [options]<br>

Options:<br>
 	 -h, --help            show this help message and exit<br>
 	 -d DURATION, --duration=DURATION Duration of bandwidth test in hours<br>
  	 -f FREQ, --freq=FREQ  Frequency of tests in minutes<br>


Defaults: <br>

Default Duration = 0 and Frequency = 0 (exactly one run) <br>

Duration = 0 will result in a single run done.<br>

Frequency = 0 will result in non stop tests for the duration. <br>








#Client Server
Tools for testing for throttling based on protocol.<br>

To start the server: <br>
python3 Server.py

To perform a test:<br>
Edit the SERVER_IP and SERVER_PORT variables in Client.py to point to the running server

Usage: Client.py [options]<br>

Options:<br>
	-h, --help	 			show the help message and exit<br>
	-p PROTOCOL, --protocol=PROTOCOL: 	Specify the protocol to use for the test<br>
	-n TRIALS, --trials=TRIALS: 		Specify the number of trials to use for the test
