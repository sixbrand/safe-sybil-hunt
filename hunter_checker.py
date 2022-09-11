import requests
import time

max_reward = 260
min_reward = 160
# get your own eth_scan api token
ETH_SCAN_API_TOKEN = ''


# 1. fetch safe wallets of which rewards are less than 150 $SAFE
# 2. get the creator of the safe wallets by calling eth_scan API

URL_TPL = 'https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses={}&apikey={}'
creators = {}  # key for wallet address, value for safe wallets created by this address


def query_creator(contracts):
    url = URL_TPL.format(','.join(contracts), ETH_SCAN_API_TOKEN)
    resp = requests.get(url).json()
    for ele in resp['result']:
        creator = ele['contractCreator']
        contract = ele['contractAddress']
        if creator not in creators:
            creators[creator] = []
        creators[creator].append(contract)
    return


wallets = []

with open(file='./safe_airdrop_order_by_reward.txt', mode='r') as f:
    lines = f.readlines()
    for line in lines:
        info = line.splitlines()[0].split(sep=',')
        wallet = info[0]
        reward = int(info[1])
        if reward < min_reward:
            continue
        if reward > max_reward:
            break
        wallets.append(wallet)
    f.close()

wallets_count = len(wallets)
print(
    f'found {wallets_count} safe wallets for reward less than {max_reward} and more than {min_reward}')


batch_size = 5
start = 0
while start+batch_size < wallets_count:
    print(f'batch query #{int(start/batch_size)}')
    query_wallets = wallets[start:start+batch_size]
    try:
        query_creator(query_wallets)
    except Exception as e:
        print("exception accured at start={}".format(str(start)))
        print(e)
    start += batch_size
    time.sleep(1)



# sort creators by how many safe wallets created
creators = sorted(creators.items(),
                  key=lambda item: len(item[1]), reverse=True)


# record
output_file = f'./safe_wallets_rewards_between_{max_reward}_n_{min_reward}.txt'
with open(file=output_file, mode='w') as f:
    f.write('num_of_safe_wallets_created,creator,safe_wallets\n')
    for ele in creators:
        f.write(str(len(ele[1])))
        f.write(';')
        f.write(ele[0])
        f.write(';')
        f.write(','.join(ele[1]))
        f.write('\n')
    f.close()
