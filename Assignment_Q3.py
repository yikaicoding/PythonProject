import threading
import time

def fibonacci(n: int) -> int:
    # Base cases for recursive Fibonacci calculation
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    # Recursive case: T(n) = T(n-1) + T(n-2) + c
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def thread_runner(n: int, results: dict, index: int, start_times: list, end_times: list):
    # Record individual thread start and end times in nanoseconds
    start_times[index] = time.time_ns()
    results[n] = fibonacci(n)
    end_times[index] = time.time_ns()

def run_multithreaded_round(round_num: int):
    targets = [35, 38, 40]
    threads = []
    results = {}
    start_times = [0] * 3
    end_times = [0] * 3

    # Spawn 3 worker threads for concurrent execution
    for i in range(3):
        t = threading.Thread(
            target=thread_runner,
            args=(targets[i], results, i, start_times, end_times)
        )
        threads.append(t)

    # Start all threads concurrently
    for t in threads:
        t.start()

    # Wait for all worker threads to finish
    for t in threads:
        t.join()

    # Calculate total elapsed time: T = t2 (last end) - t1 (first start)
    t1_first_start = min(start_times)
    t2_last_end = max(end_times)
    total_elapsed_ns = t2_last_end - t1_first_start

    print(f"Round {round_num:2d} | T = {total_elapsed_ns:>15,d} ns | Fib(35)={results[35]}, Fib(38)={results[38]}, Fib(40)={results[40]}")
    return total_elapsed_ns

def run_single_threaded_round(round_num: int):
    targets = [35, 38, 40]
    results = {}

    # Sequential execution timing
    start_time = time.time_ns()
    for n in targets:
        results[n] = fibonacci(n)
    end_time = time.time_ns()

    total_elapsed_ns = end_time - start_time

    print(f"Round {round_num:2d} | T = {total_elapsed_ns:>15,d} ns | Fib(35)={results[35]}, Fib(38)={results[38]}, Fib(40)={results[40]}")
    return total_elapsed_ns

def main():
    print("Multithreaded Fibonacci Experiment (10 Rounds)")
    print("Formula: Time_Elapsed = End_Time_Finished_Last - Start_Time_Started_First\n")

    multithreaded_times = []
    for r in range(1, 11):
        elapsed = run_multithreaded_round(r)
        multithreaded_times.append(elapsed)

    avg_multi_ns = sum(multithreaded_times) / len(multithreaded_times)
    avg_multi_sec = avg_multi_ns / 1e9

    print(f"\nAverage Multithreaded Time (across 10 rounds): {avg_multi_ns:,.2f} ns ({avg_multi_sec:.4f} s)\n\n")

    print("Single-Threaded Fibonacci Experiment (10 Rounds)\n")

    single_threaded_times = []
    for r in range(1, 11):
        elapsed = run_single_threaded_round(r)
        single_threaded_times.append(elapsed)

    avg_single_ns = sum(single_threaded_times) / len(single_threaded_times)
    avg_single_sec = avg_single_ns / 1e9

    print(f"\nAverage Single-Threaded Time (across 10 rounds): {avg_single_ns:,.2f} ns ({avg_single_sec:.4f} s)")

if __name__ == "__main__":
    main()