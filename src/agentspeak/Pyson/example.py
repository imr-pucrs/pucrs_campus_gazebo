#!/usr/bin/env python

import pyson
import pyson.runtime
import pyson.stdlib
import time

import os

actions = pyson.Actions(pyson.stdlib.actions)

# Here is the custom action go_to. 
# With this action the will be possible to ask the ROS to move the robot.
@actions.add_function(".go_to", (int,int, ))
def go_to(x,y):
	return 1

# Here the pyson instante its environment
env = pyson.runtime.Environment()


# Here is an example to instantiate the agents.

# In this example we are instantiating a new agent with the delivery_agent.asl file to the deliveryAgent variable.
with open(os.path.join(os.path.dirname(__file__), "delivery_agent.asl")) as source:
    deliveryAgent1 = env.build_agent(source, actions, name="deliveryAgent1")

with open(os.path.join(os.path.dirname(__file__), "delivery_agent.asl")) as source:
    deliveryAgent2 = env.build_agent(source, actions, name="deliveryAgent2")

with open(os.path.join(os.path.dirname(__file__), "collect_point.asl")) as source:
    collectPoint1 = env.build_agent(source, pyson.stdlib.actions, name="collectPoint1")

with open(os.path.join(os.path.dirname(__file__), "collect_point.asl")) as source:
    collectPoint2 = env.build_agent(source, pyson.stdlib.actions, name="collectPoint2")

with open(os.path.join(os.path.dirname(__file__), "ambulance_agent.asl")) as source:
    ambulance1 = env.build_agent(source, actions, name="ambulance1")

with open(os.path.join(os.path.dirname(__file__), "ambulance_agent.asl")) as source:
    ambulance2 = env.build_agent(source, actions, name="ambulance2")

with open(os.path.join(os.path.dirname(__file__), "hospital.asl")) as source:
    hospital = env.build_agent(source, pyson.stdlib.actions, name="hospital1")

with open(os.path.join(os.path.dirname(__file__), "rescue_point.asl")) as source:
    rescuePoint1 = env.build_agent(source, pyson.stdlib.actions, name="rescuePoint1")

with open(os.path.join(os.path.dirname(__file__), "rescue_point.asl")) as source:
    rescuePoint2 = env.build_agent(source, pyson.stdlib.actions, name="rescuePoint2")

with open(os.path.join(os.path.dirname(__file__), "rescue_point.asl")) as source:
    rescuePoint3 = env.build_agent(source, pyson.stdlib.actions, name="rescuePoint3")

with open(os.path.join(os.path.dirname(__file__), "rescue_point.asl")) as source:
    rescuePoint4 = env.build_agent(source, pyson.stdlib.actions, name="rescuePoint4")

# Here are examples to provide the initial positions to the building agents

# To provide the initial position to the agents, we need to instantiate a new intention.
intention = pyson.runtime.Intention()

# After we need to instantiate a new literal called "pose". In this example, the agent will receive a new literal called "pose(5,6)"
term = pyson.Literal("pose", (5, 6))

# # Here we will add the "pose" belief to the agent belief base.
pyson.runtime.add_belief(term, collectPoint1, intention)

term = pyson.Literal("pose", (7, 8))
pyson.runtime.add_belief(term, collectPoint2, intention)

term = pyson.Literal("pose", (10, 11))
pyson.runtime.add_belief(term, rescuePoint1, intention)

term = pyson.Literal("pose", (12, 13))
pyson.runtime.add_belief(term, rescuePoint2, intention)

term = pyson.Literal("pose", (14, 15))
pyson.runtime.add_belief(term, rescuePoint3, intention)

term = pyson.Literal("pose", (16, 17))
pyson.runtime.add_belief(term, rescuePoint4, intention)

term = pyson.Literal("pose", (18, 19))
pyson.runtime.add_belief(term, hospital, intention)

term = pyson.Literal("loadCapacity", [100])
pyson.runtime.add_belief(term, deliveryAgent1, intention)

term = pyson.Literal("loadCapacity", [75])
pyson.runtime.add_belief(term, deliveryAgent2, intention)

# Here is where the simulation is started
if __name__ == "__main__":
	# Here we are calling an initial execution of the environment
	env.run()

	# In this example we will call the environment execution every second inside a loop
	count = 0
	time.sleep(1)
	while(count < 100):
		env.run()

		# Here we are adding the "execute" literal to the belief base of the agents
		# A similar approach can be used to provide the position received from the ROS to the agent
		term = pyson.Literal("execute", (count, count + 1))
		intention = pyson.runtime.Intention()

		deliveryAgent1.call(pyson.Trigger.addition, pyson.GoalType.belief, term, intention)
		deliveryAgent2.call(pyson.Trigger.addition, pyson.GoalType.belief, term, intention)
		ambulance1.call(pyson.Trigger.addition, pyson.GoalType.belief, term, intention)
		ambulance2.call(pyson.Trigger.addition, pyson.GoalType.belief, term, intention)

		time.sleep(1)
		count = count + 1
