import cv2
def capture_camera(mirror=True, size=None, write=False):
    """Capture video from camera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号

    if (write == True):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        #out = cv2.VideoWriter('C:\\Users\\hal\\Documents\\tmp\\output.avi', fourcc, 20.0, (640,480))

    isFirst = True

    while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()

        # 鏡のように映るか否か
        if mirror is True:
            frame = frame[:,::-1]

        # フレームをリサイズ
        # sizeは例えば(800, 600)
        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        if (isFirst == True):
            if (write == True):
                out = cv2.VideoWriter('C:\\Users\\hal\\Documents\\tmp\\output.avi', fourcc, 20.0, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
            isFirst = False

        if (write == True):
            #frame = cv2.flip(frame,0)
            out.write(frame)

        # フレームを表示する
        cv2.imshow('camera capture', frame)

        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break

    # キャプチャを解放する
    cap.release()
    if (write == True):
        out.release()
    cv2.destroyAllWindows()

capture_camera()
#capture_camera(write=True)

