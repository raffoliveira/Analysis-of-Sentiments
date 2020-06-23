# from multiprocess import *
import multiprocess as mp

# def cube(x):
# 	return x**3

# if __name__ == '__main__':
# 	pool = mp.Pool(processes=4)
# 	print(pool)
# 	results = pool.map(cube, range(1,1000))
# 	print(results)




def print_func(continent='Asia'):
	print('The name of continent is : ', continent)

if __name__ == "__main__":  # confirms that the code is under main function
	names = ['America', 'Europe', 'Africa']
	procs = []
	# proc = Process(target=print_func)  # instantiating without any argument
	# procs.append(proc)
	# proc.start()

	# instantiating process with arguments
	for name in names:
		# print(name)
		proc = mp.Process(target=print_func, args=(name,))
		procs.append(proc)
		proc.start()

	# complete the processes
	for proc in procs:
		print(procs)
		proc.join()