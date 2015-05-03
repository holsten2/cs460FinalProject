# cs460FinalProject
Final Project for CS460

Configuration Dependencies:\n
	speedtestcli\n
	pyplot\n
	numpy\n
	A file called results.json\n

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
