import datetime
import time

import simRemote
from simRemote import SimRemote

SIMULATOR_IP = "192.168.1.153"
STARTDELAYSECONDS = 20

s = SimRemote(SIMULATOR_IP)

# Stop scenario if it is still running
if s.null().status == simRemote.ScenarioStatus.RUNNING:
    print("Scenario is running. Stop and Rewind")
    s.en(ending_type=1)

# Configure start time
start_time = datetime.datetime.now()
start_time -= datetime.timedelta(seconds=start_time.microsecond / 1e6)
start_time += datetime.timedelta(seconds=STARTDELAYSECONDS)
sec_delta = 6 - (start_time.second % 6)
start_time += datetime.timedelta(seconds=sec_delta)
s.start_time(start_time)
print("Start time is {}".format(start_time))

print("Arm scenario")
s.ar()

# Send trigger before next second. When the run command is received the simulator wait for the trigger pulse to run the scenario.
# You could use an external (e.g. GPS) trigger or an internal trigger pulse
trigger_time = start_time - datetime.timedelta(seconds=0.9)
print("Trigger scenario at time {}".format(trigger_time))
while datetime.datetime.now() < trigger_time:
    time.sleep(0.1)
s.ru()
print("Start scenario")
