import os, sys
from random import shuffle
from time import perf_counter as time  # Python > 3.3


class DiskSpeed:
    def __init__(self, path, blocks_count=128, block_size=1048576):
        self.path = path + "\\DiskSpeedTest"
        self.results = {}
        self.get_write_speed(blocks_count, block_size)
        self.get_read_speed(blocks_count, block_size)
        os.remove(self.path)

    def get_write_speed(self, blocks_count, block_size):
        f = os.open(self.path, os.O_CREAT | os.O_WRONLY, 0o777)  # Low Level I/O
        w_times = []
        for i in range(blocks_count):
            sys.stdout.write('\rWriting: {:.2f} %'.format(
                (i + 1) * 100 / blocks_count))
            sys.stdout.flush()
            buff = os.urandom(block_size)
            start = time()
            os.write(f, buff)
            os.fsync(f)
            w_times.append(time() - start)
        os.close(f)

        write_speed = blocks_count / sum(w_times)  # MB/s
        self.results['Write Speed'] = write_speed

    def get_read_speed(self, blocks_count, block_size):
        f = os.open(self.path, os.O_RDONLY, 0o777)
        # Generate Random Read Positions
        offsets = list(range(0, blocks_count * block_size, block_size))
        shuffle(offsets)

        r_times = []
        for i, offset in enumerate(offsets, 1):
            start = time()
            os.lseek(f, offset, os.SEEK_SET)  # Set Position
            buff = os.read(f, block_size)  # Read From Position
            t = time() - start
            if not buff:
                break  # If EOF Reached
            r_times.append(t)
        os.close(f)

        read_speed = blocks_count / sum(r_times)  # MB/s
        self.results['Read Speed'] = read_speed


if __name__ == "__main__":
    drive_name = input("Enter Drive Path: ")
    disk_speed = DiskSpeed(drive_name)
    results = disk_speed.results
    print("\nWrite Speed: {:.2f}MB/s".format(results['Write Speed']))
    print("Read Speed: {:.2f}MB/S".format(results['Read Speed']))
