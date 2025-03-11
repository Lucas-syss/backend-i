from contextlib import contextmanager
import logging 

# suppress the exception. 

logging.basicConfig(level=logging.INFO, filename='exceptions.log')

@contextmanager
def open_file(filename, mode):
    print(f"Opening file {filename}")
    try:
        f = open(filename, mode)
        yield f
    except FileNotFoundError:
        logging.info("Error: The file was not found.")
        pass
    except IOError:
        logging.info("Error: An I/O error occurred.")
        pass
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        pass
    finally:
        print(f"Closing file {filename}")
        f.close()

if __name__ == "__main__":
    with open_file("bla2.txt", "a") as f:
        f.write("\nAppending with context manager using @contextmanager.")