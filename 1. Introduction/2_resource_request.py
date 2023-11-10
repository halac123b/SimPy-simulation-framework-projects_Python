import simpy

def timer(env, name, resource, duration=5):
    # With statement để làm việc với Resource obj
    with resource.request() as req:
        # Request resource event
        yield req

        print('Start timer %s at %d' % (name, env.now))
        yield env.timeout(duration)
        print('End timer %s at %d' % (name, env.now))

env = simpy.Environment()

# Resource obj, là 1 resource class, đại diện cho 1 process của máy tính và yêu cầu tài nguyên CPU để chạy
# capacity changes the number of generators in the system.
server1 = simpy.Resource(env, capacity=1)
# Add 4 process to env
for i in range(4):
    env.process(timer(env, 'Timer %s' % i, server1, i+1))
env.run()