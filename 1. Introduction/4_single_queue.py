# M/M/1 queue

import random
import simpy
import numpy
import random
import statistics

random.seed(29384)  # for seed of randint function
random_seed = 42  # for seed of other random generators
new_customers = 10000  # Tổng số job sẽ đến hệ thống

# Lấy random giá trị theo phân phối Poisson cho khoảng thời gian giữa các lần arrival của numpy
# Với lambda = 6 (tức số), random các giá trị lanh quanh 6, tức 1 đơn vị thời gian có 6 job vào
lamda = 6
interarrival = numpy.random.poisson(lamda, size=None)  # Generate new customers roughly every x seconds

waitingTimes = []
serviceTimes = []
interarrivalTimes = []
lostName = []

# customer generator with interarrival times
def generator(env, number, interval, server, service_time):
    """generator generates customers randomly"""
    for i in range(number):
        # service_time=random.expovariate(): lấy random service_time theo phân phối mũ
        c = customer(env, 'Customer%02d' % i, server, service_time=random.expovariate(service_time))
        env.process(c)
        # Lấy random interval theo phân phối mũ, lúc đầu interarrival lấy theo Poisson đc bao nhiêu, ở đây lấy 1 chia, tức thời gian giữa các lần arrival
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)  # Trả lại control cho system, sau interarrival time sẽ loop và có job khác đến

def customer(env, name, server, service_time):
    # customer arrives to the system, waits and leaves
    arrive = env.now
    # print('%7.4f : Arrival time of %s' % (arrive, name))
    with server.request() as req:
        # Dấu | giữa 2 event nghĩa là sẽ return kết quả nếu 1 trong 2 event được trigger
        # req: job đã request đc resource và đang đc xử lí
        # Ở đây hoặc event đc xử lí, hoặc time-out tức job đó phải đợi và k đc xử lí

        # env.timeout(arrive): ở đây chọn time-out k hợp lí, vì quá dài, nên gần như các process đều sẽ thực hiện đc
        # result chứa event đc trigger
        results = yield req | env.timeout(arrive)

        if req in results:
            # Khi đc server, tiếp tục đợi qua service_time
            servertime = service_time
            yield env.timeout(servertime)
            serviceTimes.append(servertime)   # thêm data vào list chứa service_time
            # print('%7.4f Departure Time of %s' % (env.now, name))
            # print('%7.4f Time Spent in the system of %s' % (env.now - arrive, name))
        else: # Nếu process bị time-out (ở đây rất khó xảy ra)
            waiting_time = env.now - arrive
            waitingTimes.append(waiting_time) # thêm data vào list chứa waiting_time
            # print('%6.3f Waiting time of %s' % (waiting_time, name))

            lostName.append(name)

random.seed(random_seed)

env1 = simpy.Environment()
server1 = simpy.Resource(env1, capacity=1)  # capacity changes the number of servers in the system.

env1.process(generator(env1, new_customers, interarrival, server1, service_time=0.15))
env1.run()

interarrivalTimes.append(interarrival)

# Bước thống kê lại các dữ kiện
# Lib statistics: tính mean của 1 list
average_interarrival = statistics.mean(interarrivalTimes)
average_serviceTime = statistics.mean(serviceTimes)

print("Average Interarrival Time Is : %7.4f" % average_interarrival)
print("Average Service Time Is : %7.4f" % average_serviceTime)

if len(waitingTimes) > 0:
    average_waitingTime = statistics.mean(waitingTimes)
    print("Average Waiting Time Is : %7.4f" % average_waitingTime)

print("Lost customers: ", lostName)
print(len(interarrivalTimes))
