import requests

target_youtube_user = [
    "NoobfromuaDota2",
    "DotadigestDD"
]


def find_all(username):
    id_list = []
    sub = "watch?v="
    s = requests.get("https://www.youtube.com/c/{}/videos".format(username)).text
    index = s.find(sub)
    while index != -1:
        video_id = s[(index + 8): (index + 19)]
        id_list.append(video_id)
        index = s.find(sub, index + 1)

    if len(id_list) > 0:
        return id_list
    else:
        return -1


def init_history(video_list):
    history = open("history.txt", "a+")
    for video_id in video_list:
        history.write(str(video_id) + "\n")
    history.close()


if __name__ == "__main__":
    for username in target_youtube_user:
        video_list = find_all(username)
        if video_list is not -1:
            init_history(video_list)
