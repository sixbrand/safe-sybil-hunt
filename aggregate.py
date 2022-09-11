import csv

reader = csv.reader(
    open("./safe_airdrop.csv"))


rewards = {}

first_line = True
for line in reader:
    if first_line:
        first_line = False
        continue
    wallet = line[0]
    reward = int(float(line[1]))
    rewards[wallet] = reward


# sort safe wallets by corresponding rewards
entries = sorted(rewards.items(),
                 key=lambda item: item[1], reverse=False)


output_file = './safe_airdrop_order_by_reward.txt'
with open(file=output_file, mode='w') as f:
    for entry in entries:
        f.write(entry[0])
        f.write(',')
        f.write(str(entry[1]))
        f.write('\n')
    f.close()
