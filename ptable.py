from multiprocessing import Pool
from multiprocessing import cpu_count



def ptable(f, arglist, processes=cpu_count()):
    try:
        print ('starting the pool map')
        pool = Pool(processes=processes)  
        result = pool.map(f, arglist)  
        return result
        print ('pool map complete')
    except KeyboardInterrupt:
        print ('got ^C while pool mapping, terminating the pool')
        pool.terminate()
        print ('pool is terminated')
    except Exception:
        print ('got exception: terminating the pool')
        pool.terminate()
        print ('pool is terminated')
    finally:
        print ('joining pool processes')
        pool.close()
        pool.join()
        print ('join complete')



# tests
		
#def  f(x):
#    res= 1
#    for i in range(1000000):
#        res=res* x/(x+1)
#    return res		
#
#
#print(ptable(f, range(30), processes=10))     