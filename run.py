# To run neura
import multiprocessing


def startNeura():
    print("Process 1 is running.")
    from main import start
    start()
    
# To run hotword   
def listenHotword():
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()
    
    
    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startNeura)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")