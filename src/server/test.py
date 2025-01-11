import multiprocessing
import time
import sys
import mmap
import os
import contextlib

def background_process(shared_memory_name):
    """Function to run as a background process."""
    print("Background process started.")

    # Open the shared memory for communication
    with open(shared_memory_name, "r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 1024)) as shared_memory:
            while True:
                shared_memory.seek(0)
                message = shared_memory.read(1024).decode('utf-8').strip('\x00')
                if message:
                    if message == "stop":
                        print("Stopping background process.")
                        break
                    print(f"Received message: {message}")
                    # Clear the shared memory
                    shared_memory.seek(0)
                    shared_memory.write(b"\x00" * 1024)
                time.sleep(1)
                print('still here')

    print("End background")

if __name__ == "__main__":
    shared_memory_name = "/dev/shm/my_shared_memory"  # Use /dev/shm for shared memory on Linux

    if len(sys.argv) > 1:
        # Client mode: send a message to the shared memory
        with open(shared_memory_name, "r+b") as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 1024)) as shared_memory:
                message = sys.argv[1]
                shared_memory.seek(0)
                shared_memory.write(message.encode('utf-8').ljust(1024, b"\x00"))
                print("Message sent to background process.")
    else:
        # Server mode: start the background process
        # Create the shared memory file
        if not os.path.exists(shared_memory_name):
            with open(shared_memory_name, "wb") as f:
                f.write(b"\x00" * 1024)  # Initialize with null bytes

        # Start the background process
        process = multiprocessing.Process(target=background_process, args=(shared_memory_name,))
        # process.daemon = True
        process.start()
        print("New background process started.")

        # Keep main process alive to simulate background activity
        # try:
        #     while True:
        #         time.sleep(1)
        # except KeyboardInterrupt:
        #     print("Main process terminated.")
