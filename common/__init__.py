from redis import Redis

rd1 = Redis(host='49.235.55.221', db=1, password='123456', decode_responses=True)

# rd2用来存储临时验证用的手机号和验证码
rd2 = Redis(host='49.235.55.221', db=2, password='123456', decode_responses=True)
