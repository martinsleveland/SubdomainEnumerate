import yt_dlp

print(" ")
print("THIS MIGHT NOT BE ALLOWED! THIS IS FOR EDUCATIONAL PURPOSES ONLY!")
print("I CLAIM NO RESPONSIBILITY FOR ANY ACTIONS TAKEN ON THE DOWNLOADS MADE.")
print("I DO NOT CONDONE ANY ILLEGAL ACTIVITIES.")
print(" ")

yon = input("Can you comprehend what i wrote above? (Y/n): ")

if yon == 'Y' or yon == 'y' or yon == 'YES' or yon == 'yes' or yon == 'Yes':
    pass
else:
    print("")
    print("Exiting program...")
    exit()

def download_video(url):
    ydl_opts = {
        'format': 'mp4', # for mp4 (:
        'outtmpl': '%(title)s.%(ext)s',  # name = name + extetion
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    print("")
    video_url = input("Enter the youtube URL: ")

    download_video(video_url)

    print("works, but remember that i told you that i claim no responsibility for your actions (:")
