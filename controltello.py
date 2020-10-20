import threading
import cv2
from tello import Tellosocket
import logging
import time

logging.basicConfig(filename='state.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

pc_ip = "0.0.0.0"
pc_state_port = 8890
pc_video_port = 11111

Tello = Tellosocket(pc_ip, pc_state_port)

def receive_data():
    logger = logging.getLogger(__name__)
    while True:
        try:
            time.sleep(1)
            logger.debug(Tello.receive())
        except Exception as e:
            logger.debug(e)
            break

def send_data():
    while True:
        try:
            msg = input("")
            if "end" in msg:
                Tello.close()
                break
            Tello.send(msg)
        except KeyboardInterrupt:
            Tello.close()
            break

# capture_video
def capture_video():
    Tello.send("streamon")
    udp_video_address = 'udp://@0.0.0.0:' + str(11111)

    cap = cv2.VideoCapture(udp_video_address)
    cap.open(udp_video_address)

    while True:
        ret, frame = cap.read()
        cv2.imshow("raw frame", frame)
        key = cv2.waitKey(1)
        if key == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()

# main
def main():
    thread_receive = threading.Thread(target=receive_data)
    thread_send = threading.Thread(target=send_data)
    thread_capture = threading.Thread(target=capture_video)

    Tello.send("command")
    thread_receive.start()
    thread_send.start()
    thread_capture.start()

if __name__ == "__main__":
    main()