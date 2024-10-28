import struct
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy import stats

def fast_inverse_sqrt(x):
    x = np.float32(x)
    i = struct.unpack('i', struct.pack('f', x))[0]
    i = 0x5f3759df - (i >> 1)
    y = struct.unpack('f', struct.pack('i', i))[0]
    y = y * (1.5 - 0.5 * x * y * y)
    return y

def std_inverse_sqrt(x):
    return 1 / np.sqrt(x)


input_sizes = [1000, 5000, 10000, 50000, 100000]
fast_times = []
std_times = []

for N in input_sizes:
    x_values = np.random.random(N).astype(np.float32) * 100
    
    start_time = time.perf_counter()
    fast_results = [fast_inverse_sqrt(x) for x in x_values]
    fast_times.append(time.perf_counter() - start_time)
    
    start_time = time.perf_counter()
    std_results = [std_inverse_sqrt(x) for x in x_values]
    std_times.append(time.perf_counter() - start_time)


print("Input Size | Fast Inverse Sqrt Time (s) | Standard Inverse Sqrt Time (s)")
print("-" * 70)
for size, fast_time, std_time in zip(input_sizes, fast_times, std_times):
    print(f"{size:<10} | {fast_time:<26.6f} | {std_time:<26.6f}")


log_sizes = np.log(input_sizes)
log_fast_times = np.log(fast_times)
log_std_times = np.log(std_times)

fast_slope, _, _, _, _ = stats.linregress(log_sizes, log_fast_times)
std_slope, _, _, _, _ = stats.linregress(log_sizes, log_std_times)

print("\nTime Complexity Analysis:")
print(f"Fast Inverse Sqrt: O(n^{fast_slope:.3f})")
print(f"Standard Inverse Sqrt: O(n^{std_slope:.3f})")


N = 100000
x_values = np.random.random(N).astype(np.float32) * 100
fast_results = np.array([fast_inverse_sqrt(x) for x in x_values])
std_results = np.array([std_inverse_sqrt(x) for x in x_values])

relative_error = np.abs((fast_results - std_results) / std_results)
max_relative_error = np.max(relative_error)
mean_relative_error = np.mean(relative_error)
median_relative_error = np.median(relative_error)

print("\nAccuracy Analysis:")
print(f"Maximum Relative Error: {max_relative_error:.8f}")
print(f"Mean Relative Error: {mean_relative_error:.8f}")
print(f"Median Relative Error: {median_relative_error:.8f}")

# Plotting
plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.plot(input_sizes, fast_times, 'o-', label='Fast Inverse Square Root')
plt.plot(input_sizes, std_times, 'o-', label='Standard Inverse Square Root')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Input Size (N)')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time Comparison')
plt.legend()
plt.grid(True)

plt.subplot(122)
plt.hist(relative_error, bins=50, edgecolor='black')
plt.xlabel('Relative Error')
plt.ylabel('Frequency')
plt.title('Distribution of Relative Errors')
plt.grid(True)

plt.tight_layout()
plt.show()


print("\nAdditional Analysis:")
print(f"Fast method is on average {np.mean(np.array(fast_times) / np.array(std_times)):.2f} times slower than the standard method")
print(f"Percentage of results with relative error < 1%: {np.mean(relative_error < 0.01) * 100:.2f}%")
print(f"Percentage of results with relative error < 0.1%: {np.mean(relative_error < 0.001) * 100:.2f}%")
