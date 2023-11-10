import simpy


def timer(env, name, resource, duration=5):
    with resource.request() as req:
        yield req

        print('Start timer %s at %d' % (name, env.now))
        yield env.timeout(duration)
        print('End timer %s at %d' % (name, env.now))

def final_msg(msg, list_of_processes):
    # event nhận arg là 1 list process khác, trigger khi tất cả event trong list process đều đã trigger
    # fail nếu có bất kì event nào k đc trigger
    yield simpy.AllOf(env, list_of_processes)
    print(env.now, msg)

listp = []
env = simpy.Environment()
# capacity changes the number of generators in the system.
server1 = simpy.Resource(env, capacity=1)
for i in range(4):
    listp.append(env.process(timer(env, 'Timer %s' % i, server1, i+1)))
# env.process(final_msg("All done", listp))
env.run()