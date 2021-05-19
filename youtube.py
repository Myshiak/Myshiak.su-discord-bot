from urllib.request import urlopen
from json import load


def allVideos(channelId: str, titles: bool = False):
    api_key = 'AIzaSyBaE8ll1hZvBJlUKTQGsmW2WwF5Cno6IcE'
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    first_url = base_search_url + f'key={api_key}&channelId={channelId}&part=snippet,id&order=date&maxResults=25'
    video_links = []
    url = first_url
    while True:
        inp = urlopen(url)  # print(url)
        resp = load(inp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                if titles:
                    stats = get_information_from_youtube_video(i['id']['videoId'])
                    listS = [base_video_url + i['id']['videoId'], i['id']['videoId'], i['snippet']['title'], i['snippet']['publishTime']]
                    for stat in stats['items'][0]['statistics']:
                        listS.append(stat + ' ' + stats['items'][0]['statistics'][stat])
                    video_links.append(listS)
                else:
                    video_links.append([base_video_url + i['id']['videoId']])
        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links


def get_information_from_youtube_video(video_id):
    api_key = "AIzaSyBaE8ll1hZvBJlUKTQGsmW2WwF5Cno6IcE"
    base_info_url = 'https://www.googleapis.com/youtube/v3/videos?'
    info_url = base_info_url + f'part=statistics&key={api_key}&id={video_id}'
    inp = urlopen(info_url)
    resp = load(inp)
    return resp


if __name__ == '__main__':
    for video in allVideos(channelId='UC2D-WeF4oMlyjlGq7hjRe9g', titles=True):
        print(video)
