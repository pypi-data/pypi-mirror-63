import re

# Static helper methods


def parse_playlist_items(results, owned=False):
    songs = []
    count = 1
    for result in results:
        count += 1
        if 'musicResponsiveListItemRenderer' not in result:
            continue
        data = result['musicResponsiveListItemRenderer']
        videoId = None

        try:
            # if playlist is not owned, the playlist item can't be interacted with
            if owned:
                for item in data['menu']['menuRenderer']['items']:
                    if 'menuServiceItemRenderer' in item and 'playlistEditEndpoint' in item['menuServiceItemRenderer']['serviceEndpoint']:
                        setVideoId = item['menuServiceItemRenderer']['serviceEndpoint']['playlistEditEndpoint']['actions'][0]['setVideoId']
                        videoId = item['menuServiceItemRenderer']['serviceEndpoint']['playlistEditEndpoint']['actions'][0]['removedVideoId']
                        break
            else:
                videoId = data['overlay']['musicItemThumbnailOverlayRenderer']['content']['musicPlayButtonRenderer']['playNavigationEndpoint']['watchEndpoint']['videoId']
                setVideoId = None


            artist = data['flexColumns'][1]['musicResponsiveListItemFlexColumnRenderer']['text']['runs'][0]['text']
            title = data['flexColumns'][0]['musicResponsiveListItemFlexColumnRenderer']['text']['runs'][0]['text']
            song = {'videoId': videoId, 'artist': artist, 'title': title, 'setVideoId': setVideoId}
            songs.append(song)
        except Exception as e:
            print("Item " + str(count) + ": " + str(e))

    return songs


def parse_search_result(data, resultType = None):
    search_result = {}
    default = not resultType
    if not resultType:
        resultType = get_item_text(data, 1).lower()
        # default to album since it's labeled with multiple values ('Single', 'EP', etc.)
        if resultType not in ['artist', 'playlist', 'song', 'video']:
            resultType = 'album'

    if resultType in ['song', 'video']:
        search_result['videoId'] = data['overlay']['musicItemThumbnailOverlayRenderer']['content'][
            'musicPlayButtonRenderer']['playNavigationEndpoint']['watchEndpoint']['videoId']
        search_result['title'] = get_item_text(data, 0)
        search_result['artist'] = get_item_text(data, 1 + default)

    if resultType in ['artist', 'album', 'playlist']:
        search_result['browseId'] = data['navigationEndpoint']['browseEndpoint']['browseId']

    if resultType in ['artist']:
        search_result['artist'] = get_item_text(data, 0)

    elif resultType in ['album']:
        search_result['title'] = get_item_text(data, 0)
        search_result['type'] = get_item_text(data, 1)
        search_result['artist'] = get_item_text(data, 2)
        search_result['year'] = get_item_text(data, 3)

    elif resultType in ['playlist']:
        search_result['title'] = get_item_text(data, 0)
        search_result['author'] = get_item_text(data, 1 + default)
        search_result['itemCount'] = get_item_text(data, 2 + default).split(' ')[0]

    elif resultType in ['song']:
        hasAlbum = len(data['flexColumns']) == 4
        if hasAlbum:
            search_result['album'] = get_item_text(data, 2 + default)
        search_result['duration'] = get_item_text(data, 2 + hasAlbum + default)

    elif resultType in ['video']:
        search_result['views'] = get_item_text(data, 2 + default).split(' ')[0]
        search_result['duration'] = get_item_text(data, 3 + default)

    search_result['resultType'] = resultType

    return search_result


def get_item_text(item, index):
    return item['flexColumns'][index]['musicResponsiveListItemFlexColumnRenderer']['text']['runs'][0]['text']


def html_to_txt(html_text):
    tags = re.findall("<[^>]+>",html_text)
    for tag in tags:
        html_text = html_text.replace(tag,'')
    return html_text