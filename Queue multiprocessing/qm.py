from multiprocessing import Queue, Process
import time


def handler(queue):
    msg = str()
    while msg != 'net':
        msg = queue.get()
        if msg == 'da':
            print('receive da')
    print('receive net')


def sender(queue):
    for i in range(5):
        print('send da')
        queue.put('da')
        time.sleep(2)
    print('send net')
    queue.put('net')


if __name__ == '__main__':
    queue = Queue()
    sender_p = Process(target=sender, args=(queue,))
    sender_p.start()
    handler_p = Process(target=handler, args=(queue,))
    handler_p.start()

    handler_p.join()
    sender_p.join()

    queue.close()
    queue.join_thread()
