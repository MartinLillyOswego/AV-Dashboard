# AV-Dashboard
This project is intended to give a user the ability to connect with the “wooden racer” autonomous vehicle. It will provide a graphical user interface that simulates a modern vehicle’s dashboard.


# First-time setup
1. Install python version 3.7 from the microsoft store. If you install it through some other means, the important thing is that you can run "python3.7 somerandomfilehere.py" in a batch script and not get an error.
2. Run setup.bat either by double clicking it or running it in command prompt(make sure you execute it from the directory of setup.bat).
3. Run start.bat (should have appeared in the same directory). Two things will happen. A browser window will open and a command prompt window will open. In the command prompt window, you might see the following error:
  Communication: Failed to connect to serial port could not open port 'COM2': FileNotFoundError(2, 'The system cannot find the file specified.', None, 2)
This means one of two things: a) either the radio is not connected to your device or b) the radio connected to a different port than the default. If the problem is b), go the dashboard that opened in the browser and click on the configuration button in the top right corner. In the Tuning Menu that opens, the first field will be "Radio's Serial Port". The default operating value is "COM4". You will need to change this to the port your radio has connected to. In the windows search bar, type 'device manager' and open it. There will be a 'PORTS' field which you can expand. Figure out which device is the radio and look for COM#. This is what you must type into the field in the tuning menu. After clicking submit, close both the browser window and the command prompt window. Launch start.bat again and it should work.
