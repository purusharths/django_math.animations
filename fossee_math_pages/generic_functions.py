IMGSIZE = 2097152 #2MB
VIDSIZE = 31457280 #30MB

def large_img_size(img):
    if img.size > IMGSIZE:
        return True
    else:
        return False

def large_video_size(video):
    if video.size > VIDSIZE:
        return True
    else:
        return False
    