import discum
from json_extract import GetValue2

yourtoken = str(input("Input your discord token (it must be in the server you want to scrape) : "))
channelid = str(input("Input channel id: "))
serverid = str(input("Input server id: "))
bot = discum.Client(token=yourtoken, log=False)

bot.gateway.resetMembersOnSessionReconnect = False 

def fetch(resp, guild_id, use_op8=False, wait=1):
     if bot.gateway.finishedMemberFetching(guild_id):
          bot.gateway.removeCommand({'function': fetch, 'params': {'guild_id': guild_id, 'use_op8':use_op8, 'wait':wait}})
          num_members = bot.gateway.session.guild(guild_id).members
      
          
          print('Finished member fetching. Fetched {} members from guild {}'.format(len(num_members), guild_id))
          bot.gateway.close()

def get_members(guild_id, channel_id, wait=1): 
	print('scraping members...')
	bot.gateway.fetchMembers(guild_id, channel_id, keep="all", reset=False, wait=wait)
	bot.gateway.command({'function': fetch, 'params': {'guild_id': guild_id, 'wait':wait}})
	bot.gateway.run()
	return bot.gateway.session.guild(guild_id).members

members = list(get_members(serverid, channelid).keys())
for ids in members:
     getobj = GetValue2(bot.getProfile(ids).json())
     getobj = getobj.get_values('connected_accounts')
     
     if getobj is not None: 
          
          try:
               for i in range(len(getobj)):
                    if getobj[i]['type'] == 'twitter':
                         print(getobj[i]['id'])
                         with open('twitter.txt', 'a') as f:
                              f.write(getobj[i]['id'] + '\n')
          except KeyError:
               pass

