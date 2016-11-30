import csv

STRUCTURE_PATH = 'course-217-structure.csv'
EVENTS_PATH = 'course-217-events.csv'
TOP_NUM = 10

step_cost = {}
with open(STRUCTURE_PATH) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'course_id':
            continue
        step_cost[int(row[5])] = int(row[-1])

print('Maximum points per course', sum(step_cost.values()))

events = []
with open(EVENTS_PATH) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'user_id':
            continue

        events.append(row)
events.sort(key=lambda x: x[3])

user_points = {}
start_time = {}
course_time = {}
finished_users = set()
for row in events:
    user_id = int(row[0])
    if user_id == 2649:
        print(row)
    if user_id in finished_users:
        continue
    if user_id not in start_time:
        start_time[user_id] = int(row[3])
        user_points[user_id] = 0

    if row[1] == 'passed':
        user_points[user_id] += step_cost[int(row[2])]

    if user_points[user_id] >= 24:
        course_time[user_id] = int(row[3]) - start_time[user_id]
        finished_users.add(user_id)

top = sorted(course_time.items(), key=lambda x: x[1])
result = []
for elem in top[:TOP_NUM]:
    result.append(str(elem[0]))

print('Result:', ','.join(result))
