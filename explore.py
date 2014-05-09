import redis
import msgpack

def redis_factory():
    return redis.StrictRedis()

def setup():
    db = redis_factory()
    if 1:
        return
    users = db.smembers('users')
    for user in users:
        compute_events(db, user)

def compute_events(db, user, max_event_delay=10.):
    times = [score for _, score in db.zrange(user + ':times', 0, -1, withscores=True)]
    db.delete(user + ':events')
    if not times:
        return
    events = [{'start_time': times[0], 'unique_times': 1, 'stop_time': times[0]}]
    last_time = times[0]
    for t in times[1:]:
        if t - last_time > max_event_delay:
            events.append({'start_time': t, 'unique_times': 0})
        events[-1]['stop_time'] = t
        events[-1]['unique_times'] += 1
        last_time = t
    db.set(user + ':events', msgpack.dumps(events))
    print(events)
    return events

if __name__ == '__main__':
	setup()
