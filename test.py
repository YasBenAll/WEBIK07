import json

following = '''
{
    "following": [
    2, 3, 4
    ]
}
'''

data = json.loads(following)
print(data)
data['following'].append(1)
follow = json.dumps(data["following"])
print(follow)
follow2 = json.dumps(follow)
print(follow2)