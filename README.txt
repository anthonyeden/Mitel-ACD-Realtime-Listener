Mitel ACD Listener
------------------------------------------------------------------------------------------
Developed by Anthony Eden / Hope Media Ltd

Hope Media:    http://hopemedia.com.au/
Anthony Eden:  http://mediarealm.com.au/

Based on the specs provided by the
Mitel Networks - Data Services - Programmer Reference
http://www.mitel.com/resources/tech_data_services_prog_ref.pdf

v1.0


INTRODUCTION
------------------------------------------------------------------------------------------
This Python script listens to the Mitel ACD Real Time Events stream, parses it, and
provides it in JSON format for other applications to consume (such as display boards and
reporting tools).

Mitel 3300 ICP systems provide access to the ACD RTE Stream via an IP connection to the
ICP at port 15373.


REQUIREMENTS
------------------------------------------------------------------------------------------
 * Mitel ACD Real Time Events stream capable phone system
 * Python 2.7
 * Apple OS X or Windows (Linux has not been tested but may work)


TESTING THE MITEL ACD REAL TIME EVENTS STREAM
------------------------------------------------------------------------------------------
To test that this stream is available in your Mitel system, you can use a Telnet command:
telnet 192.168.201.2 15373
(ensure you substitute in the IP Address of your Mitel system)

Upon connecting to this stream, you should immediately see data appear in your Telnet
console, such as "74R13024320140115". In this example, the first two characters are the
numerical identifier of the data, and "R" signifies a keep-alive packet.

Performing actions on an ACD-enabled phone, such as logging on, answering a call, placing
a call or logging off will show different data in your Telnet console.

Refer to the document "Mitel Networks - Data Services - Programmer Reference" for full
details on the format of each data packet.


PROGRAM SETUP
------------------------------------------------------------------------------------------
0. Confirm your phone system meets the requirements.
1. Download and install Python on your computer.
2. Copy the mitelacd.py and mitel_data.json files to a directory on your computer
   e.g. "C:\MitelACD\" or "/Users/anthony/MitelACD/"
3. Change the IP address in mitelacd.py to the IP address of your Mitel system (line 8)
   This must be the IP address you checked with Telnet in the above section.
4. Run the mitelacd.py file (double click if you have Windows file associations setup,
   or use your command line).
5. Confirm that mitel_data.json is being written to by performing actions on an
   ACD-enabled phone and checking the file modified timestamp. You will see some data sent
   to your Python console window, but please note no keep-alive packets are written to the
   console

Setup is now complete. This application must keep running to read the stream and write the
results to the file.


MITEL_DATA.JSON
------------------------------------------------------------------------------------------
Once you have started running your script you can develop further applications to consume
this file. There are four sections to this file:
 * Paths
 * Agents
 * Groups
 * Last Updated Timestamp

Each agent can have the status "in", "out", "busy", "idle", and "timer". When creating a
simple available/busy indicator it is best to group these status together. "in" and "idle"
both mean the ACD Agent is available to take a call. "busy" and "timer" mean the ACD Agent
is unavailable to take a call, but logged on. "out" means the agent is not logged on and
thus can't take calls.

Groups and paths show similar data. Depending on how your Mitel system is setup determines
which one you should use. It is suggested you start by using the "groups" and change this
if you find some data is being incorrectly reported.

The "waiting" field shows how many people are in the queue. This field is a fixed length
and ranges from "000" to "999".

The "agents" field shows how many agents are logged on at the present time. This field is
a fixed length and ranges from "000" to "999".

The "longestwait" field shows in MM:SS how long the longest queue member has been in the
queue. For example, a value "0015" means a caller has been waiting for 15 seconds. This
will remain as as "0000" when no one is in the queue.

The timestamp is the last time the file was updated, stored as a floating point Unix Epoch
timestamp. Although it is a floating point number, some systems will not support precision
greater than one second.

There are some values written in the sample JSON file. You may remove these before starting
your application to ensure only data specific to your site is stored in the file.


RUNNING AS A BACKGROUND APPLICATION
------------------------------------------------------------------------------------------
How you setup this program as a background application is up to you. Indeed, you don't
even need to run it in the background. You could leave the terminal window running in a
desktop session.

In a Windows environment the easiest way to set it up as a background application is to
set up a scheduled task which runs on system boot. This means it will run as soon as the
computer starts up. Assuming there are no bugs in the application, it should keep running
indefinitely.

This application has proven to be reliable over inbound call center periods with as many
as 11 agents active on calls at once and with many more in the queue. As the whole
processing loop is wrapped in a try/catch block, invalid stream data and file system
errors will be ignored.


SUPPORT, WARRANTY, ETC.
------------------------------------------------------------------------------------------
Please contact the developer directly for support. This software must not be distributed
to third-parties without written consent. Enquiries for licensing should be directed to
the developer.


THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.






