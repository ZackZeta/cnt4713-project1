# CNT-4731 Project 1

Project 1 FIU CNT-4731
## Provided Files

`client.py`, `server-s.py`, and  `server.py` are the entry points for the client, simplified server, and server parts of the project.

## TODO


## Problems
part 1:
1.Initial problem was setting up the framework for the project.
2.Could not connect server and client following example.
3.ports needed to be deleted because they were left open through the terminal.
-run CMD
-netstat -ano (to get list of connections)
-taskkill /F /PID <PID> (to terminate the process)
4.VSC running two programs at once was not always working.
5.Find a way to send data in binary to the server
6.argv is not working going to try to use argparse
7.trying to figure out how to do timeouts and modifying code 

part 2:
1.Trying to figure out how server handles incorrect port through more than just except
2.Cant get server to end gracefully 
## Acknowledgements 

Course Material was mainly following was used to expand and reinforced what was learned.

freeCodeCamp.org. (2018). Learn Python - Full Course for Beginners [Tutorial]. YouTube. from https://www.youtube.com/watch?v=rfscVS0vtbw&amp;t=4793s&amp;ab_channel=freeCodeCamp.org.

Tech With Tim. (2020). Python Socket Programming Tutorial. YouTube. from https://www.youtube.com/watch?v=3QiPPX-KeSc&amp;ab_channel=TechWithTim.

GeeksforGeeks. (2022, November 18). With statement in Python. GeeksforGeeks. from https://www.geeksforgeeks.org/with-statement-in-python/

Python - read and write files. Python - Read and Write Files. (n.d.). from https://www.tutorialsteacher.com/python/python-read-write-file 

part 2:
1. Server is not receiving data 
2. cant figure out how to have server receiving multiple confections. 
3. Sever cant connect to multiple so cant have 10 connections
4. time out is not working as intended
5. unable to figure out the rest of the tests without the other ones working

part 3:
1. too many issues had to rebuild the program from scratch again to test each case.
2. could not get the server to receive data
3. server cannot accept more connections due to the above issue tried dispite it.

