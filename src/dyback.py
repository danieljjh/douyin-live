"""
 douyin backend
"""
import json
import requests
import time
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import os
import fileinput


import matplotlib.pyplot as plt

import re

pd.set_option('display.max_rows', 200)
sns.set_theme(style="darkgrid")

outfolder = "./pkls"


def get_json(string):
  """
  获取字符串里第一个 “{” 和最后一个 “}” 的内容并转换成 JSON

  Args:
    string: 字符串

  Returns:
    JSON 对象
  """

  # 匹配第一个 “{” 和最后一个 “}”
  match = re.search(r"{.*}", string)
  if match is None:
    return None

  # 获取匹配的内容
  content = match.group()
  # 将内容转换成 JSON 对象
  json_object = json.loads(content)

  return json_object


def decode_gift(data):
  badgeList = data['user'].get('BadgeImageList', [])
  badge = 0
  user_level = 0
  if len(badgeList) > 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    user_level = int(badgeList[1].get('content').get('level'))
  elif len(badgeList) == 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  elif len(badgeList)  > 0:
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  s = {
    'userID': data['user']['id'],
    'nickName': data['user']['nickName'],
    'displayId': data['user'].get('displayId', ''),
    'userLevel': user_level,
    'badge': badge,
    'userFollowing': data['user']['FollowInfo']['followingCountStr'],
    'userFollower': data['user']['FollowInfo']['followerCountStr'],
    'giftName': data['gift'].get('describe', ''),
    'giftD': data['gift']['diamondCount'],
    # 'combo': data['gift'].get('combo', False),
    'sendType':data.get('sendType', None),
    'clientGiftSource':data['clientGiftSource'],
    'time':data.get('sendTime', None),
    'timeStr': data['time']
  }
  return s


def decode_member(data):
  """进入直播间消息"""
  badgeList = data['user'].get('BadgeImageList', [])
  badge = 0
  user_level = 0
  if len(badgeList) > 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    user_level = int(badgeList[1].get('content').get('level'))
  elif len(badgeList) == 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  elif len(badgeList)  > 0:
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  s = {
    'userID': data['user']['id'],
    'nickName': data['user']['nickName'],
    'displayId': data['user'].get('displayId', ''),
    # 'gender': data['user']['gender'],
    'userLevel': user_level,
    'badge': badge,
    'userFollowing': data['user']['FollowInfo']['followingCountStr'],
    'userFollower': data['user']['FollowInfo']['followerCountStr'],
    'action': data['action'],
    'memberCount': int(data.get('memberCount', '0')),
    'timeStr': data['time']

  }  
  return s


def decode_chat(data):
  """chat"""
  s = {
    'userID': data['user']['id'],
    'nickName': data['user']['nickName'],
    'displayId': data['user'].get('displayId', ''),
    # 'gender': data['user']['gender'],
    # 'userLevel': data['user']['Level'],
    'userFollowing': data['user']['FollowInfo']['followingCountStr'],
    'userFollower': data['user']['FollowInfo']['followerCountStr'],
    # 'action': data['action'],
    'content': data['content'],
    'time': data['eventTime'],
    'timeStr': data['time']

  } 
  return s

def decode_rmuser(data):
    """decode_rmuser"""

    s = {
      'total': int(data.get('total', 0)),
      'totalUser': int(data.get('totalUser', 0)),
      'timeStr': data['time']
    } 
    return s

def decode_social(data):
  """关注消息"""
  badgeList = data['user'].get('BadgeImageList', [])
  badge = 0
  user_level = 0
  if len(badgeList) > 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    user_level = int(badgeList[1].get('content').get('level'))
  elif len(badgeList) == 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  elif len(badgeList)  > 0:
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  s = {
    'userID': data['user']['id'],
    'nickName': data['user']['nickName'],
    'displayId': data['user'].get('displayId', ''),
    'gender': data['user'].get('gender', 0),
    'userLevel': user_level,
    'badge':badge,
    'userFollowing': data['user']['FollowInfo']['followingCountStr'],
    'userFollower': data['user']['FollowInfo']['followerCountStr'],
    'action': data.get('action', '0'),
    'timeStr': data['time']
  } 
  return s

def decode_like(data):
  """点赞消息"""
  badgeList = data['user'].get('BadgeImageList', [])
  badge = 0
  user_level = 0
  if len(badgeList) > 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    user_level = int(badgeList[1].get('content').get('level'))
  elif len(badgeList) == 2:
    badge = badgeList[-1].get('content').get('level', '0')
    badge = int(badge)
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  elif len(badgeList)  > 0:
    try:
      user_level = int(badgeList[0].get('content').get('level'))
    except:
      user_level = 0
  s = {
    'userID': data['user']['id'],
    'nickName': data['user']['nickName'],
    'displayId': data['user'].get('displayId', ''),
    'gender': data['user'].get('gender', 0),
    'userLevel': user_level,
    'badge':badge,
    'userFollowing': data['user']['FollowInfo']['followingCountStr'],
    'userFollower': data['user']['FollowInfo']['followerCountStr'],
    'count': int(data.get('count', '0')),
    'total': int(data.get('total', '0')),
    'timeStr': data['time']
  } 
  return s

def decode_ranklist(line):
  """
    rank list
  """
  timestr =  line.split(" - INFO -")[0]
  match = re.search(r"\[.*\]", line)
  if match is not None:
    # 获取匹配的内容
    content = match.group()
    # 将内容转换成 JSON 对象
    json_object = json.loads(content)
    res = {
      'timeStr': timestr,
      'ranklist': json_object
    }
    return res



def process_log(fname, outfolder):
    fdate = fname.split("_")[1][:-4]
    ftime = fname.split("_")[1][11]
    dfname = f"{fname.split('_')[-1][:10]}_2" if ftime=='2' else f"{fname.split('_')[-1][:10]}_1"


    with open(fname) as f:
        lines = f.readlines()

    gifts = []
    chats = []
    member = []
    rmuser = []
    social = []
    ranklist = []
    likes = []

    for line in lines[:]:
        # print(line)  
        try:
          if "unPackWebcastGiftMessage" in line:
              # print(line)  
              timestr =  line.split(" - INFO -")[0]
              data = get_json(line)
              data.update({"time": timestr})
              decoded = decode_gift(data)
              gifts.append(decoded)
          elif "unPackWebcastMemberMessage" in line:
              timestr =  line.split(" - INFO -")[0]
              data = get_json(line)
              data.update({"time": timestr})
              decoded = decode_member(data)
              member.append(decoded)

          elif "unPackWebcastChatMessage" in line:
              timestr =  line.split(" - INFO -")[0]
              data = get_json(line)
              data.update({"time": timestr})
              decoded = decode_chat(data)
              chats.append(decoded)
          elif "WebcastRoomUserSeqMessage" in line:
              timestr =  line.split(" - INFO -")[0]
              data = get_json(line)
              data.update({"time": timestr})
              decoded = decode_rmuser(data)
              rmuser.append(decoded)
          elif "unPackWebcastSocialMessage" in line:
              """ 新 关注 """
              timestr =  line.split(" - INFO -")[0]
              data = get_json(line)
              data.update({"time": timestr})
              try:
                decoded = decode_social(data)
                social.append(decoded)
              except:
                print(data)
          elif "unPackWebcastLikeMessage" in line:
              timestr =  line.split(" - INFO -")[0]
              data = get_json(line)
              data.update({"time": timestr})
              decoded = decode_like(data)
              likes.append(decoded)
          elif "更新打赏排行" in line:
              """ 更新打赏排行 """
              try:
                  data = decode_ranklist(line)
                  ranklist.append(data) 
              except:
                  pass       
        except:
            pass   
    gifts_df = pd.DataFrame(gifts)
    chats_df = pd.DataFrame(chats)
    member_df = pd.DataFrame(member)
    rmuser_df = pd.DataFrame(rmuser)
    social_df = pd.DataFrame(social)
    social_df = social_df[social_df.action == '1']
    likes_df = pd.DataFrame(likes)
    ranklist_df = pd.DataFrame(ranklist)

    rmuser_df.loc[:, 'tr'] = rmuser_df.timeStr.apply(lambda x: dt.datetime.strptime(x[:-4], "%Y-%m-%d %H:%M:%S" ))
    rmuser_df = rmuser_df.set_index('tr')
    gifts_df.loc[:, 'tr'] = gifts_df.timeStr.apply(lambda x: dt.datetime.strptime(x[:-4], "%Y-%m-%d %H:%M:%S" ))
    member_df.loc[:, 'tr'] = member_df.timeStr.apply(lambda x: dt.datetime.strptime(x[:-4], "%Y-%m-%d %H:%M:%S" ))
    

    gifts_df.to_pickle(f"{outfolder}/{dfname}_gifts.pkl")
    chats_df.to_pickle(f"{outfolder}/{dfname}_chats.pkl")
    member_df.to_pickle(f"{outfolder}/{dfname}_member.pkl")
    rmuser_df.to_pickle(f"{outfolder}/{dfname}_rmuser.pkl")
    social_df.to_pickle(f"{outfolder}/{dfname}_social.pkl")
    likes_df.to_pickle(f"{outfolder}/{dfname}_likes.pkl")
    ranklist_df.to_pickle(f"{outfolder}/{dfname}_ranklist.pkl")

    # print(f"gifts {len(gifts)}, chats {len(chats)}  member {len(member)}, rmuser_df {len(rmuser_df)},  social_df {len(social_df)}")
    
    # new fans
    new_fans = social_df[social_df.action == "1"].shape[0]
    print("Date ", fdate)
    print(f"新粉丝  {new_fans}")
    # total room user
 
    # rmuser_df = rmuser_df.set_index('tr')
    rmuser_df_2 = rmuser_df.resample('5min').agg({'total':'mean', 'totalUser':'max'}).dropna()
    try:
        rmuser_df_2 = rmuser_df_2.astype(int)
        rmss = rmuser_df_2[rmuser_df_2.total >=100]
        if len(rmss) >=2:
            duration100 = round((rmss.index[-1]- rmss.index[0]).total_seconds() / 3600, 2)
        else:
            duration100 = 0
    except:
        print("error" , fname)
        duration100 = 0
    total_visitor = rmuser_df.totalUser.max()
    room_mean = int(rmuser_df.total.mean())
    print(f"场观 {total_visitor}, 平均人数 {room_mean}, 最高 {rmuser_df.total.max()}")
    print(f" 100 人以上持续时间 {duration100} 小时")
    totalgift = gifts_df.giftD.sum()
    gift_by_user = gifts_df.groupby(['nickName']).agg({'giftD':'sum', 'timeStr':'count'})
    giftuser = gift_by_user.shape[0]
    # small gift user sum
    small_gift = gift_by_user.loc[gift_by_user.giftD < 600]
    big_gift = gift_by_user.loc[gift_by_user.giftD > 600]
    print(f"total Gifts {totalgift}, 送礼人数 {gift_by_user.shape[0]}")
    print(f"small gift user: {small_gift.shape[0]}, value {small_gift.giftD.sum()}, {(small_gift.giftD.sum()/totalgift):.2f}")
    print(f"big gift user: {big_gift.shape[0]}, value {big_gift.giftD.sum()}, {(big_gift.giftD.sum()/totalgift):.2f}")
    
    # return gifts_df, member_df, rmuser_df,social_df, ranklist_df
    return dict(
        fdate = fdate,
        ftime = ftime,
        new_fans = new_fans,
        total_visitor = total_visitor,
        room_mean = room_mean,
        room_max = rmuser_df.total.max(),
        duration100 = duration100,
        totalgift = totalgift,
        giftuser = giftuser
    )
    
    
def read_history(outfolder, dayStr, timeStr):
    dfname = f"{outfolder}/{dayStr}_{timeStr}"
    dfs = ["gifts_df", "member_df", "rmuser_df","social_df", "likes_df"]
    
    gifts_df = pd.read_pickle(f"{outfolder}/{dayStr}_{timeStr}_gifts.pkl")    
    member_df = pd.read_pickle(f"{outfolder}/{dayStr}_{timeStr}_member.pkl")    
    rmuser_df = pd.read_pickle(f"{outfolder}/{dayStr}_{timeStr}_rmuser.pkl")    
    social_df = pd.read_pickle(f"{outfolder}/{dayStr}_{timeStr}_social.pkl")    
    likes_df = pd.read_pickle(f"{outfolder}/{dayStr}_{timeStr}_likes.pkl")
    return gifts_df, member_df, rmuser_df,social_df, likes_df


def get_key_features(outfolder,dayStr, timeStr, toPrint=False):
    gifts_df, member_df, rmuser_df,social_df, likes_df = read_history(outfolder, dayStr, timeStr)
    # new fans
    new_fans = social_df[social_df.action=="1"].shape[0]
    high_level_fans = social_df[social_df.userLevel>30].shape[0]
    # total room user
    visitor_high =  member_df[member_df.userLevel>39]
    visitor_high_num = visitor_high.groupby('displayId').agg({'nickName':'last', 'userLevel':'last','tr':['count', 'min', 'max'], }).shape[0]
    # rmuser_df = rmuser_df.set_index('tr')
    rmuser_df_2 = rmuser_df.resample('5min').agg({'total':'mean', 'totalUser':'max'}).dropna()
    try:
        rmuser_df_2 = rmuser_df_2.astype(int)
        rmss = rmuser_df_2[rmuser_df_2.total >=100]
        if len(rmss) >=2:
            duration100 = round((rmss.index[-1]- rmss.index[0]).total_seconds() / 3600, 2)
        else:
            duration100 = 0
    except:
        print("error" , fname)
        duration100 = 0
    total_visitor = rmuser_df.totalUser.max()
    room_mean = int(rmuser_df.total.mean())

    totalgift = gifts_df.giftD.sum()
    gift_by_user = gifts_df.groupby(['displayId']).agg({'giftD':'sum', 'timeStr':'count'})
    giftuser = gift_by_user.shape[0]
    # small gift user sum
    small_gift = gift_by_user.loc[gift_by_user.giftD < 100]
    big_gift = gift_by_user.loc[gift_by_user.giftD > 100]
    if toPrint:
        print("Date ", fdate)
        print(f"新粉丝  {new_fans}")
        print(f"场观 {total_visitor}, 平均人数 {room_mean}, 最高 {rmuser_df.total.max()}")
        print(f" 100 人以上持续时间 {duration100} 小时")    
        print(f"total Gifts {totalgift}, 送礼人数 {gift_by_user.shape[0]}")
        print(f"small gift user: {small_gift.shape[0]}, value {small_gift.giftD.sum()}, {(small_gift.giftD.sum()/totalgift):.2f}")
        print(f"big gift user: {big_gift.shape[0]}, value {big_gift.giftD.sum()}, {(big_gift.giftD.sum()/totalgift):.2f}")
    return dict(
        dayStr = dayStr,
        timeStr = timeStr,
        new_fans = new_fans,
        high_level_fans = high_level_fans,
        visitor_high_num = visitor_high_num,
        total_visitor = total_visitor,
        room_mean = room_mean,
        room_max = rmuser_df.total.max(),
        duration100 = duration100,
        totalgift = totalgift,
        giftuser = giftuser,
        small_gift_user =small_gift.shape[0],
        small_gift_value = small_gift.giftD.sum(),
        small_gift_pct =round(small_gift.giftD.sum()/totalgift, 2),
        big_gift_user =big_gift.shape[0],
        big_gift_value = big_gift.giftD.sum(),
        big_gift_pct =round(big_gift.giftD.sum()/totalgift, 2),
    )
    
    
def diamond_adjust(giftName):
  """
  zzgift.loc[:, 'giftD'] = zzgift.giftName.apply(diamond_adjust)
  """
  diamond = {
        '送出钻石火箭': 12000,
        '送出钻石邮轮': 7200,
        '送出钻石飞机': 3600,
        '送出钻石跑车': 1500,
        '送出钻石兔兔': 360,
        
    }
  return diamond.get(giftName)