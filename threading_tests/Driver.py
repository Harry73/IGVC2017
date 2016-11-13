from Consumer import Consumer
from Producer import Producer
from threading import Thread, Semaphore

# Trying out a standard solution for the producer-consumer concurrency paradigm.
# Counting semaphores n and s maintain proper access to the data structure.
# In this case my data structure is a list, but I will use it as a stack.
# The printing is a little messed up, though I'm not sure why.
def main():
	stack = []
	n = Semaphore(0)
	s = Semaphore(1)
	
	# Create Producer and Consumer threads
	producer1 = Producer(stack, n, s, 1)
	producer2 = Producer(stack, n, s, 2)
	producer3 = Producer(stack, n, s, 3)
	producer4 = Producer(stack, n, s, 4)
	producer5 = Producer(stack, n, s, 5)
	consumer = Consumer(stack, n, s)
	
	# Start all the threads
	producer1.start()
	producer2.start()
	producer3.start()
	producer4.start()
	producer5.start()
	consumer.start()
	
	# Wait for threads to finish
	producer1.join()
	producer2.join()
	producer3.join()
	producer4.join()
	producer5.join()
	consumer.join()
	
	print("Done.")

if __name__ == "__main__":
	main()