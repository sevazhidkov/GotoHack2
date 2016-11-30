import csv
import tqdm

STRUCTURE_PATH = 'course-217-structure.csv'
EVENTS_PATH = 'course-217-events.csv'

events = []
with open(EVENTS_PATH) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'user_id':
            continue

        row[0] = int(row[0])
        events.append(row)
events.sort(key=lambda x: x[3])

steps = {}
with open(STRUCTURE_PATH) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'course_id':
            continue
        steps[int(row[5])] = (int(row[2]), int(row[4]), int(row[6]))

steps = list(sorted(steps.items(), key=lambda x: x[1]))

steps_num = {}
i = 0
for step in steps:
    steps_num[step[0]] = i
    i += 1

returned_users = {}
all_users = {}
last_step = {}
user_steps = {}

for event in tqdm.tqdm(events):
    user_id = int(event[0])
    step_num = steps_num[int(event[2])]
    all_users[step_num] = all_users.get(step_num, set()).union({user_id})
    if user_id not in user_steps:
        user_steps[user_id] = [step_num]
        continue

    find_i = False
    find_ii = False
    for step in user_steps[user_id]:
        if step == step_num:
            find_i = True
        if find_i and step == step_num + 1:
            find_ii = True
            break
    if find_ii:
        returned_users[step_num] = returned_users.get(step_num, set()).union({user_id})

    user_steps[user_id].append(step_num)
    last_step[user_id] = step_num


ability = {}
for step_id, step_num in tqdm.tqdm(steps_num.items()):
    try:
        ability[step_id] = len(returned_users.get(step_num, set())) / len(all_users.get(step_num, set()))
    except ZeroDivisionError:
        continue

print(list(sorted(ability.items(), key=lambda x: x[1], reverse=True))[:10])
print(','.join(map(lambda x: str(x[0]),
                   list(sorted(ability.items(), key=lambda x: x[1], reverse=True))[:10])))
