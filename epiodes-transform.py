import json
import os
import re

ep_json = open('./episodes.json')

eps = json.load(ep_json)

episode_map = {}
for ep in eps:
    # print ep['title']
    # print ep['id']
    rs = re.match("Episode (\d+)", ep['title'])
    if rs:
        ep_num = rs.group(1)
        episode_map[ep_num] = ep

for filename in os.listdir('./source/_posts'):
    file = open('./source/_posts/%s' % filename, "r")
    content = file.read()
    file.close()
    m = re.search(r'title: "Episode (\d+)', content, re.S)
    if m:
        # look for listen block
        pattern = r'\* <a href="http:\/\/devhell\.s3\.amazonaws\.com\/ep(\d+)-128stereo.mp3" rel="enclosure">(Download|Listen) now (\([^\)]+\))<\/a>.*\s+?\n\s+?<audio controls src="http:\/\/devhell\.s3\.amazonaws\.com\/ep(\d+)-128stereo\.mp3">'
        m = re.search(pattern, content)
        if m:
            episode = m.group(1)
            stats = m.group(3)
            new_episode_id = episode_map[episode]['id']
            print "%s -> %s" % (m.group(1), new_episode_id)
            replace_str = '<iframe frameborder="0" height="36px" scrolling="no" seamless src="https://simplecast.com/e/%s?style=dark" width="100%%"></iframe>\n<a href="http://audio.simplecast.com/%s.mp3" rel="enclosure">Download now %s</a>' % (new_episode_id, new_episode_id, stats)
            # print replace_str
            new_content = re.sub(pattern, replace_str, content)
            print new_content
            # file = open('./source/_posts/%s' % filename, "w")
            # file.write(new_content)
            # file.close()
