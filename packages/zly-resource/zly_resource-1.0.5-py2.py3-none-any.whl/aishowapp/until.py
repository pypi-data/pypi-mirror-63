# -*- coding: utf-8 -*-
import time
import requests
import json

from flask import g

import requests
import json

from aishowapp.ext import cache


def get_permission():
    res = requests.get('http://127.0.0.1:9999/api/permission/?token=123&name=zly')
    response = json.loads(res.content)
    print(response, type(response))
    return response


def require_frequency(func):
    def wrapper(*args, **kwargs):
        name = g.name
        print('name', name, type(name))
        lis = cache.get(name)
        times = time.time()
        print('list', lis)
        # user=User.query.filter(User.username==name).first()
        # role_r_name = [item.r_name for item in user.roles][0]
        # print('role_r_name',role_r_name,type(role_r_name))
        if lis:
            res = {'permission':'c'}
            # print(res, type(res))
            if res['permission'] == 'c':
                if len(lis) < 3:
                    lis.append(times)
                    cache.set(name, lis, timeout=7 * 24 * 60 * 60)
                    print(len(lis), lis)
                    return func(*args, **kwargs)
                else:
                    # print('list', list)
                    frist_time = lis[0]
                    chai_time = times - frist_time
                    print('1', chai_time)
                    if chai_time >= 7:
                        lis.pop(0)
                        lis.append(times)
                        cache.set(name, lis, timeout=7 * 24 * 60 * 60)
                        print('时间已过', lis)
                        # 60 * 60 * 24 * 7
                        return func(*args, **kwargs)
                    else:
                        # usersearch = UserSearch.query.all()[-1]
                        return {'code': 20001, 'message': '普通用户一周只能更改三次,请您提升权限'}
            else:
                print('admin')
                lis.append(times)
                cache.set(name, lis, timeout=7 * 24 * 60 * 60)
                return func(*args, **kwargs)
        else:
            cache.set(name, [time.time()], timeout=7 * 24 * 60 * 60)
            print('first list', cache.get)
            return func(*args, **kwargs)

    return wrapper

