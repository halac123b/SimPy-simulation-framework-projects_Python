import simpy

# 1 hàm trong đó có yield event đc gọi là 1 process
def timer(env, duration=5):
    while True:
        # Environment.now: thời điểm hiện tại của simulation
        print('Start timer at %d' % env.now)

        # Dùng yield generate 1 simpy event, ở đây timeout() là 1 event sẽ trả lại control cho hệ thống 1 khoảng thời gian, sau đó quay lại chạy process này tiếp
        yield env.timeout(duration)
        print('End timer at %d' % env.now)

# Khởi tạo env mô phóng
env = simpy.Environment()
# Environment.process(<process>): đăng kí 1 process vào hệ thống
env.process(timer(env, 3))
# Start hệ thống (ở đây có giới hạn thời gian)
env.run(until=20)