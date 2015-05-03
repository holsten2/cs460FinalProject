# cs460FinalProject
Final Project for CS460

Configuration Dependencies:\n
	speedtestcli\n
	pyplot\n
	numpy\n
	A file called results.json\n

#Client Server
Tools for testing for throttling based on protocol.

To start the server:
python3 server.py

To perform a test:
Edit the SERVER_IP and SERVER_PORT variables in Client.py to point to the running server

Usage: Client.py [options]

Options:
	-h, --help	 			show the help message and exit
	-p PROTOCOL, --protocol=PROTOCOL: 	Specify the protocol to use for the test
	-n TRIALS, --trials=TRIALS: 		Specify the number of trials to use for the test
